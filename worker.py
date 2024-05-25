from Data.Celery import initCelery
from Data.Models import Endpoint, User
from Data.Database import initSQLAlchemy
from utils import isHealthy, shouldRaiseAlert, send_alert, getHealth, setHealth, clamp
from flask import Flask

flask = Flask(__name__)

db = initSQLAlchemy(flask)

celery = initCelery("worker")

@celery.task
def check_health(endpoint_id):
    with flask.app_context():
        endpoint: Endpoint = Endpoint.query.get(endpoint_id) # type: ignore
        
        if endpoint is None:
            print(f"endpoint {endpoint_id} not found")
            return
        
        health_status = isHealthy(
            url=endpoint.url,
            method=endpoint.method,
            headers=endpoint.headers,
            success_criteria_status_code=endpoint.success_criteria_status_code,
            success_criteria_response_time=endpoint.success_criteria_response_time
        )
        print(f"Endpoint with id {endpoint_id} is {'health' if health_status == True else 'unhealth'}")
        
        previous_health = getHealth(endpoint_id)
        
        if previous_health is None:
            setHealth(endpoint_id, 100)
            return
        
        if health_status == False:
            raise_alert = shouldRaiseAlert(endpoint_id, previous_health, endpoint.unhealthy_threshold_count)
        
            if raise_alert:
                user = User.query.get(endpoint.owner)
                
                if not user:
                    print(f"User not found for endpoint with id {endpoint.id}, Failed sending email alert")
                    return
                
                print("sending alert")
                send_alert(
                    email=user.email,
                    url=endpoint.url
                )
        else:
            health = clamp(0, previous_health + 100/endpoint.unhealthy_threshold_count, 100)
            setHealth(endpoint_id, health)
        
        
                
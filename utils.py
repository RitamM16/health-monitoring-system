import requests
import time
from Data.Redis import redis

def isHealthy(
    url: str,
    method: str,
    headers: dict,
    success_criteria_status_code: int,
    success_criteria_response_time: int
) -> bool:
    response = None
    
    start_time = time.time()
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        else:
            response = requests.post(url, headers=headers)
        end_time = time.time()
        
        if response.status_code != success_criteria_status_code:
            return False
        
        if end_time - start_time > success_criteria_response_time:
            return False
        
    except Exception as e:
        print(e)
        return False
    
    return True

def shouldRaiseAlert(id: str, previous_health: float, threshold: int) -> bool:

    if previous_health == 0:
        return False
    else:
        calculated_health = previous_health - 100/threshold
        print(f"calculated HealthCheck", calculated_health)
        if calculated_health <= 0:
            setHealth(id, 0)
            return True
        else:
            setHealth(id, calculated_health)
        
    return False

def clamp(minimum, x, maximum):
    return max(minimum, min(x, maximum))
    

def getHealth(id: str) -> float | None:
    health = redis.get(id)
    return health if health is None else float(health)  # type: ignore
    
def setHealth(id: str, amount: float) -> None:
    redis.set(id, amount, ex=60*60)
    
def send_alert(email: str, url: str):
    import smtplib
    from email.mime.text import MIMEText

    msg = MIMEText(f"The endpoint {url} is down!")
    msg['Subject'] = 'API Endpoint Down'
    msg['From'] = 'monitoring@test.com'
    msg['To'] = email

    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()
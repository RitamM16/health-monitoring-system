from config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND_URL, MYSQL_CONN_STRING, MYSQL_CELERY_CONN_STRING
from celery import Celery
from sqlalchemy_celery_beat.session import SessionManager
from sqlalchemy_celery_beat.models import PeriodicTask, IntervalSchedule, Period, PeriodicTaskChanged, update
import json

def initCelery(moduleName: str):
    celery = Celery(
        moduleName,
        backend=CELERY_RESULT_BACKEND_URL,
        broker=CELERY_BROKER_URL
    )
    
    celery.conf.update({

        'beat_dburi': MYSQL_CELERY_CONN_STRING,

        'beat_schema': "scheduler"

    })
    
    return celery

def createHealthCheck(id: str, interval: int):
    session_manager = SessionManager()
    engine, Session = session_manager.create_session(MYSQL_CELERY_CONN_STRING)
    session = Session()
    
    schedule = session.query(IntervalSchedule).filter_by(every=interval, period=Period.SECONDS).first()

    if not schedule:
        schedule = IntervalSchedule(every=interval, period=Period.SECONDS) # type: ignore #
        session.add(schedule)
        session.commit()
    
    task = PeriodicTask(
        schedule_model=schedule,
        name=id,
        task="worker.check_health",
        args=json.dumps([id])
    )

    session.add(task)
    session.commit()
    
def removeHealthCheck(id: str):
    session_manager = SessionManager()
    engine, Session = session_manager.create_session(MYSQL_CELERY_CONN_STRING)
    session = Session()
    stmt = update(PeriodicTask).where(PeriodicTask.name == id, PeriodicTask.enabled == True).values(enabled=False)
    session.execute(stmt)
    session.commit()
    
    PeriodicTaskChanged.update_from_session(session)
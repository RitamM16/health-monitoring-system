#!/bin/bash

SELECTION=$1

if [ -z "$SELECTION" ]
then
    SELECTION="SERVER"
fi

if [ $SELECTION == "SERVER" ]
then
    echo "starting api server"
    poetry run gunicorn app:app --bind 0.0.0.0:5001
elif [ $SELECTION == "SCHEDULER" ]
then
    echo "running scheduler"
    poetry run celery -A scheduler:celery beat -S sqlalchemy -l info
elif [ $SELECTION == "WORKER" ]
then
    echo "running workers"
    poetry run celery -A worker:celery worker -S sqlalchemy -l info
else
    echo "wrong command"
fi
#!/bin/bash

# Run beat scheduler `-B` and send events `-E`
CELERY_ARGS="-B -E"

# Configure queues
CELERY_QUEUES=${CELERY_QUEUES:-"celery,notifications"}
CELERY_ARGS="$CELERY_ARGS -Q $CELERY_QUEUES"

# Set log level
CELERY_LOG_LEVEL=${CELERY_LOG_LEVEL:-"info"}
CELERY_ARGS="$CELERY_ARGS -l $CELERY_LOG_LEVEL"

# Reload tasks when source changes?
if [ "$CELERY_RELOAD" ]; then
    CELERY_ARGS="$CELERY_ARGS --autoreload"
fi

echo "Starting Celery with args: $CELERY_ARGS"
python runcelery.py worker $CELERY_ARGS

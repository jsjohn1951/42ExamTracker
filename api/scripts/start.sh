#! /bin/sh

cd /app

uvicorn main:app --proxy-headers --reload --host 0.0.0.0 --port 15400
# gunicorn -w 4 -k uvicorn.workers.UvicornWorker --proxy-headers --host 0.0.0.0 --port 15400
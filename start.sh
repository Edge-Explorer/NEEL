#!/bin/bash
export PYTHONPATH=$PYTHONPATH:.
echo "PYTHONPATH is $PYTHONPATH"
ls -R
uvicorn backend.main:app --host 0.0.0.0 --port $PORT

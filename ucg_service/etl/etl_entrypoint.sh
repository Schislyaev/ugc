#!/bin/sh

mkdir -p logs
export PYTHONPATH="${PYTHONPATH}:/opt/app"
python3.10 etl/etl_service.py
#!/usr/bin/env bash
SERVICE_DIR=/home/administrator/demography
PY=${SERVICE_DIR}/venv/bin/python3
IMPORT_DIR=/home/administrator/demography_import

cd ${SERVICE_DIR} && ${PY} manage.py import ${IMPORT_DIR}

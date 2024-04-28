#!/bin/bash
cd ./src && uvicorn main:app --reload --port 8001 --host 0.0.0.0 --env-file ../.env
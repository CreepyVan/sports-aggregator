#!/bin/bash
cd sports_aggregator
uvicorn app.main:app --host 0.0.0.0 --port 8000
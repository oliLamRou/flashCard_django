#!/usr/bin/env bash

source ../.venv/bin/activate
python -m uvicorn flashcard.asgi:application --reload


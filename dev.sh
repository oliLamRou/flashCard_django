#!/usr/bin/env bash

cd ./backend
python -m uvicorn flashcard.asgi:application --reload &

cd ..

cd ./frontend
npm run dev
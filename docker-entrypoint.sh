#!/bin/bash

# Start the API server in the background
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &

# Start the documentation server
cd docs/_build/html && python -m http.server 8080 
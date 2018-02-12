#!/bin/bash

# Install new dependencies
pip install -r requirements.txt && \

# Verify configuration setup
python setup.py

exec "$@"
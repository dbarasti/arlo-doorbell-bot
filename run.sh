#!/bin/bash

# set env variables
export $(grep -v '^#' .env | xargs)

# enable venv
source venv/bin/activate

python3 runner.sh

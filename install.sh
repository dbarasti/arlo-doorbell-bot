#!/bin/bash

# setup virtualenv
python3 -m venv venv
source venv/bin/activate

# install requirements 
pip3 install -r requirements.txt

# set env variables
export $(grep -v '^#' .env | xargs)



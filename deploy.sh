#!/bin/bash

source ~/.virtualenvs/freedemy/bin/activate
cd "$(dirname "$0")"
git pull
pip install -r requirements.txt

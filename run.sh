#!/bin/bash

source ~/.virtualenvs/freedemy/bin/activate
cd "$(dirname "$0")"
exec python main.py

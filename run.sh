#!/bin/bash

source ~/.virtualenvs/freedemy/bin/activate
cd "$(dirname "$0")/freedemy"
exec python main.py

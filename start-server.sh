#!/bin/bash

export FLASK_ENV=development
#export FLASK_APP=main.py
export FLASK_APP=__init__.py
 
cd lca_tool && python3 -m flask  run --host=0.0.0.0

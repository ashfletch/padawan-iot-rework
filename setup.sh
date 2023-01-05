#!/bin/bash
find ./ -name requirements.txt -exec cat {} \; -exec echo ""\; | uniq -u | tail -n +2 | tr -d "\t\r" > requirements.txt
if [ ! -d .venv ]; then
    python3 -m venv .venv
    source .venv/bin/activate
else 
    source .venv/bin/activate
fi
pip install -r requirements.txt

#!/bin/bash
export $(grep -v '^#' .env 2>/dev/null | xargs) 2>/dev/null
python3 tracker.py

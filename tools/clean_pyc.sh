#!/usr/bin/env bash
find . -type f -name "*.pyc" -exec rm {} \;
find . -type d -name "__pycache__" -exec rm -rf {} \;
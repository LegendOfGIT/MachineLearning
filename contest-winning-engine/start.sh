#!/usr/bin/env bash
set -e

docker run --rm -v $(PWD):/app -w /app -p 5000:5000 contest-winning python /app/api.py

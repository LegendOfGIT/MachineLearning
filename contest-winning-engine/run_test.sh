#!/usr/bin/env bash
set -e

docker run --rm -v $(PWD):/app -w /app contest-winning python /app/winning-engine-test.py

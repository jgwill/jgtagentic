#!/bin/bash
set -e
IMG=jgtagentic-test

# Build the wheel if not present
echo "[INFO] Building wheel..."
make dist

# Build Docker image
echo "[INFO] Building Docker image..."
docker build -t $IMG .

# Run container with config mount
echo "[INFO] Running tests in Docker with $HOME/.jgt mounted..."
docker run --rm -v $HOME/.jgt:/root/.jgt $IMG 
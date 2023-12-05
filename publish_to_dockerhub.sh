#!/bin/bash
docker buildx create --use
docker buildx build --platform=linux/amd64,linux/arm64 --tag "devforth/tobedo:latest" --tag "devforth/tobedo:1.0.7" --push .
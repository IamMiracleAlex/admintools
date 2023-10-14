#!/bin/bash
set -x
set -eu
set -o pipefail

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 066954119569.dkr.ecr.us-east-1.amazonaws.com
docker build -t admintools-clery -f Dockerfile-cel .
docker tag admintools-clery:latest 066954119569.dkr.ecr.us-east-1.amazonaws.com/admintools-clery:latest
docker push 066954119569.dkr.ecr.us-east-1.amazonaws.com/admintools-clery:latest
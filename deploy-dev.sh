#!/bin/bash
set -x
set -eu
set -o pipefail

export AWS_ACCESS_KEY_ID=$AWS_DEV_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=$AWS_DEV_SECRET_ACCESS_KEY

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 354405606653.dkr.ecr.us-east-1.amazonaws.com
docker build -t admin-tool_dev .
docker tag admin-tool_dev 354405606653.dkr.ecr.us-east-1.amazonaws.com/admin-tool_dev:latest
docker push 354405606653.dkr.ecr.us-east-1.amazonaws.com/admin-tool_dev:latest
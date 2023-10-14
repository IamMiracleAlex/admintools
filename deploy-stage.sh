#!/bin/bash
set -x
set -eu
set -o pipefail

export AWS_ACCESS_KEY_ID=$AWS_STAGING_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=$AWS_STAGING_SECRET_ACCESS_KEY

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 665654742887.dkr.ecr.us-east-1.amazonaws.com
docker build -t admin-tool_staging .
docker tag admin-tool_staging:latest 665654742887.dkr.ecr.us-east-1.amazonaws.com/admin-tool_staging:latest
docker push 665654742887.dkr.ecr.us-east-1.amazonaws.com/admin-tool_staging:latest
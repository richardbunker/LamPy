#! /bin/bash

# Deploy LamPy
# This script is used to deploy the LamPy application to AWS.

# Set the AWS profile via argument
if [ -z "$1" ]; then
  echo "Please provide an AWS profile. (default, dev, prod)"
  exit 1
fi

# Set the terraform plan/apply action via argument
if [ -z "$2" ]; then
  echo "Please provide a terraform action. (plan/apply)"
  exit 1
fi

# 1. Build the application
./build.sh

# 2. Deploy the application
cd ./terraform
AWS_PROFILE=$1 terraform $2 -var-file=./vars.tfvars

#! /bin/bash

# Remove the old deployment.zip if it exists
if [ -f deployment.zip ]; then
  rm deployment.zip
fi

cd ./src
zip -r ../deployment.zip . -x "*__pycache__/*" -x "server.py"


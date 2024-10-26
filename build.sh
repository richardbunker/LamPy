#! /bin/bash

# Get the current directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Remove the old deployment.zip if it exists
echo -e "\n♻️  Cleaning up old deployment...\n"
if [ -f deployment.zip ]; then
  rm deployment.zip
fi

# Add the python site_packages to the deployment package
echo -e "🛠️ Installing dependencies...\n"
source ./.venv/bin/activate
pip3 install -q -r requirements.txt

# Format the code
echo -e "💅 Formatting code...\n"
black . -q
deactivate

echo -e "📀 Packaging deployment...\n"
# Add the site_packages to the deployment package
cd ./.venv/lib/python3.12/site-packages
zip -rq ../../../../deployment.zip . -x "*__pycache__/*" -x "black*/*" -x "_black*" 
# Add the source code to the deployment package
cd $DIR/src
zip -rq ../deployment.zip . -x "*__pycache__/*" -x "server.py"


echo -e "📦 Deployment package created!\n"


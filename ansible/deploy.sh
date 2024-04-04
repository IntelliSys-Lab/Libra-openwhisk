#!/bin/bash
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Exit immediately if a command exits with a non-zero status.
set -e

ENVIRONMENT=local

export OW_DB=CouchDB
export OW_DB_USERNAME=admin
export OW_DB_PASSWORD=admin
export OW_DB_PROTOCOL=http
export OW_DB_HOST=149.165.154.213
export OW_DB_PORT=5984

ansible-playbook -i environments/$ENVIRONMENT setup.yml


cd ..
./gradlew distDocker


cd ansible
# Define the environment variable
ENVIRONMENT=local  # replace 'your_environment' with your actual environment name

# Run Ansible playbooks
sudo ansible-playbook -i environments/$ENVIRONMENT couchdb.yml
sudo ansible-playbook -i environments/$ENVIRONMENT initdb.yml
sudo ansible-playbook -i environments/$ENVIRONMENT wipe.yml
sudo ansible-playbook -i environments/$ENVIRONMENT openwhisk.yml

# Installs a catalog of public packages and actions
sudo ansible-playbook -i environments/$ENVIRONMENT postdeploy.yml

# To use the API gateway
sudo ansible-playbook -i environments/$ENVIRONMENT apigateway.yml
sudo ansible-playbook -i environments/$ENVIRONMENT routemgmt.yml

wsk -i action create hello ../actions/hello.js
wsk -i action create mem ../actions/mem.js --memory 512
wsk -i action create mem_intensive mem_intensive.js --memory 512

echo "All playbooks executed successfully!"


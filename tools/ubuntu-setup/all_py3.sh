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

#  This script can be tested for validity by doing something like:
#
#  docker run -v "${OPENWHISK_HOME}:/openwhisk" ubuntu:trusty \
#    sh -c 'apt-get update && apt-get -y install sudo && /openwhisk/tools/ubuntu-setup/all.sh'
# ...but see the WARNING at the bottom of the script before tinkering.


set -e
set -x

JAVA_SOURCE=${1:-"open"}
SOURCE="${BASH_SOURCE[0]}"
SCRIPTDIR="$( dirname "$SOURCE" )"

echo "*** installing basics"
/bin/bash "$SCRIPTDIR/misc.sh"

echo "*** installing python dependencies"
pip3 install argcomplete
pip3 install couchdb
pip3 install redis
pip3 install numpy
pip3 install psutil
pip3 install docker
pip3 install pandas
pip3 install torch
pip3 install sklearn
pip3 install couchdb

echo "*** installing java"
/bin/bash "$SCRIPTDIR/java8.sh" $JAVA_SOURCE

echo "*** installing ansible"
pip install --upgrade setuptools pip
pip install markupsafe
pip install ansible==2.5.2
pip install jinja2==2.9.6
pip install docker==2.2.1    --ignore-installed  --force-reinstall
pip install httplib2==0.9.2  --ignore-installed  --force-reinstall
pip install requests==2.10.0 --ignore-installed  --force-reinstall


echo "*** installing npm"
/bin/bash "$SCRIPTDIR/npm.sh"


echo "*** installing ssh dependencies"
/bin/bash "$SCRIPTDIR/ssh.sh"


echo "*** installing redis tools"
sudo apt install -y redis-tools

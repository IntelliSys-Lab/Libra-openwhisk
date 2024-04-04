#! /bin/bash
set -e

rm -rf build
rm -rf virtualenv

sudo docker run --rm -v "$PWD:/tmp" openwhisk/python3action bash \
  -c "cd tmp && virtualenv virtualenv && source virtualenv/bin/activate && pip3 install -r requirements.txt"

mkdir build

cp -R __main__.py ./build
cp -R virtualenv ./build
cd ./build
zip -X -r ./index.zip *



wsk -i action update hi --kind python:3 --main main --memory 64 index.zip
cd ..

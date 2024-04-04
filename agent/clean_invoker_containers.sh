#! /bin/bash

cd ../ansible 
sudo ansible-playbook -i environments/local clean_invoker_containers.yml
cd ../agent

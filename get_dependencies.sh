#!/bin/bash
echo "Automating the dependency installation for the script...."
sudo apt-get update -y && sudo apt-get upgrade -y
sudo apt-get install python3 python3-dev python3-pip git vim openssl libmysqlclient-dev -y
git config --global user.email "musyoki.tralah@students.jkuat.ac.ke"
git config --global user.name "TralahM"
alias pip=pip3
alias python=python3
pip3 install sqlalchemy  pandas numpy mysqlclient
echo "Done with dependencies..."
echo "\n Setting up crontab....."
export EDITOR=vim
cp fetch_matches.py ~/remote_mysqldb_updater.py
crontab -e

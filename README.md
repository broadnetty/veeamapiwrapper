# veeamapiwrapper

Wrapper for Veeam for Cloud api 


To enable auto-setup, you need to prepare your base VBA image first:

- create a folder /home/ubuntu/veeam-setup
- create there a file init.sh and put there the following:

#!/bin/bash
echo "Starting script.." &> /home/ubuntu/veeam-setup/setup.log
cd /home/ubuntu/veeam-setup
rm -rf veeamapiwrapper
git clone git@github.com:broadnetty/veeamapiwrapper.git
/usr/bin/python3 veeamapiwrapper/main.py &>> /home/ubuntu/veeam-setup/setup.log


git@github.com:broadnetty/veeamapiwrapper.git is the path to your repository where you forkd this repo to

- setup the crontab by adding the following line:
@reboot sleep 40 && /home/ubuntu/veeam-setup/init.sh

- edit the /etc/environment file and append this lines:

export VBAlogin="your web UI VBA admin user"
export VBApass="your password for this user"
export VBAhost="127.0.0.1"
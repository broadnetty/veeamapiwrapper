# veeamapiwrapper

Wrapper for Veeam for Cloud api 


To enable auto-setup, you need to prepare your base VBA image first:
- fork this repository to your GitHub account
- create a folder /home/ubuntu/veeam-setup
- create there a file init.sh and put there the following:

>#!/bin/bash
>if [ -f /home/ubuntu/veeam-setup/not_first_run ]; then
>  echo "Starting script.." &> /home/ubuntu/veeam-setup/setup.log
>  cd /home/ubuntu/veeam-setup
>  rm -rf veeamapiwrapper
>  git clone git@github.com:broadnetty/veeamapiwrapper.git
>  /usr/bin/python3 veeamapiwrapper/main.py &>> /home/ubuntu/veeam-setup/setup.log
>  touch /home/ubuntu/veeam-setup/not_first_run
>fi

The git@github.com:broadnetty/veeamapiwrapper.git is the path to your repository where you forked this repo to.
You should also replace all entries of 'veeamapiwrapper' in the init.sh with your repository name. 

- setup the crontab by adding the following line:
@reboot sleep 40 && /home/ubuntu/veeam-setup/init.sh

- edit the /etc/environment file and append this lines:

export VBAlogin="your web UI VBA admin user"
export VBApass="your password for this user"
export VBAhost="127.0.0.1"

- generate a key for access your repository with (email sohuld be the same as in your account):
ssh-keygen -t ed25519 -C "your_email@example.com"

- cat the .pub file of the key and copy it for the next step
cat ~/.ssh/id_ed25519.pub

- paste the pub key content to the Github -> Repo Name -> Settings -> Deploy keys -> Add Deploy key

- create an AMI from that machine and use this AMI in your terraform templates

The setup script kicks off only by the first boot of the machine. It crates flag file and checks if it exists before doing anything:
if [ -f /home/ubuntu/veeam-setup/not_first_run ]

If you remove this file manually, the setup will go on the next boot

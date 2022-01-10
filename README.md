# veeamapiwrapper

Wrapper for Veeam for Cloud api 


To enable auto-setup, you need to prepare your base VBA image first:
- fork this repository to your GitHub account
- create a folder /home/ubuntu/veeam-setup
- create there a file init.sh and put there the following:

>#!/bin/bash<br />
>if [ ! -f /home/ubuntu/veeam-setup/not_first_run ]; then<br />
>&nbsp;&nbsp;echo "Starting script.." &> /home/ubuntu/veeam-setup/setup.log<br />
>&nbsp;&nbsp;cd /home/ubuntu/veeam-setup<br />
>&nbsp;&nbsp;rm -rf veeamapiwrapper<br />
>&nbsp;&nbsp;git clone git@github.com:broadnetty/veeamapiwrapper.git<br />
>&nbsp;&nbsp;/usr/bin/python3 veeamapiwrapper/main.py &>> /home/ubuntu/veeam-setup/setup.log<br />
>&nbsp;&nbsp;touch /home/ubuntu/veeam-setup/not_first_run<br />
>fi


The git@github.com:broadnetty/veeamapiwrapper.git is the path to your repository where you forked this repo to.
You should also replace all entries of 'veeamapiwrapper' in the init.sh with your repository name. 

- setup the crontab by adding the following line:
@reboot sleep 40 && /home/ubuntu/veeam-setup/init.sh

- edit the /etc/environment file and append this lines:

>export VBAlogin="your web UI VBA admin user"<br />
>export VBApass="your password for this user"<br />
>export VBAhost="127.0.0.1"<br />

- install the follwing packets:
>sudo apt install python3 python3-requests python3-urllib3

- generate a key for access your repository with (email sohuld be the same as in your account):
>ssh-keygen -t ed25519 -C "your_email@example.com"

- cat the .pub file of the key and copy it for the next step
>cat ~/.ssh/id_ed25519.pub

- paste the pub key content to the Github -> Repo Name -> Settings -> Deploy keys -> Add Deploy key

- create an AMI from that machine and use this AMI in your terraform templates

- IMPORTANT: you may need to start the script manually to agree the ssh key from server and remove additional files (at last on mentioned below and the veeamwrapper folder)

The setup script kicks off only by the first boot of the machine. It crates flag file and checks if it exists before doing anything:
>if [ ! -f /home/ubuntu/veeam-setup/not_first_run ]

If you remove this file manually, the setup will go on the next boot

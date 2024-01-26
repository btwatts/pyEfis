#!/bin/bash

#this is a comment
# A quick installer that pulls down the existing files from github, internet connection required
# This is a temporary tool to make testing easier.
# You will need a previously flashed raspberry pi running raspbian/raspios.
# Place this file in your user's home directory (should be what's selected by default when you download it).

#updoot yer shit
if [[ "$EUID" -ne 0 ]]; then
	echo "Sorry, you need to run this as root"
	exit 2
fi
apt update 
apt upgrade -y
apt autoremove -y
apt autoclean

apt install python3-full git unzip wget
apt install python3-pyqt6

#make base directory
mkdir ~/Avionics
cd ~/Avionics

#Install some python stuff
pip install wheel --break-system-packages
pip install PyQt6 --break-system packages

#Get some git 
git clone https://github.com/makerplane/FIX-Gateway.git
cd Fix-Gateway

pip install . --break-system-packages

cd ~/Avionics

#Install pyAvTools
git clone https://github.com/makerplane/pyAvTools.git
cd pyAvTools
pip install . --break-system-packages

cd ~/Avionics

git clone https://github.com/btwatts/pyEfis.git
cd pyEfis
pip install . --break-system-packages

cd ~/Avionics

# Get the CIFP Database
wget https://aeronav.faa.gov/Upload_313-d/cifp/CIFP_240125.zip
mkdir -p pyEfis/CIFP
unzip CIFP_240125.zip -d pyEfis/CIFP/

#tada, downloaded all the things!

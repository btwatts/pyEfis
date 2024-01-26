#!/bin/bash

#this is a comment
# A quick installer that pulls down the existing files from github, internet connection required
# This is a temporary tool to make testing easier.
# You will need a previously flashed raspberry pi running raspbian/raspios.
# Place this file in your user's home directory (should be what's selected by default when you download it).

#updoot yer shit
sudo apt update 
sudo apt upgrade -y
sudo apt autoremove -y
sudo apt autoclean

sudo apt install python3-full git unzip wget
sudo apt install python3-pyqt6

#make base directory
mkdir ~/Avionics
cd ~/Avionics

#Install some python stuff
pip install wheel --break-system-packages
pip install PyQt6 --break-system packages

#Get some git 
git clone https://github.com/makerplane/FIX-Gateway.git
cd Fix-Gateway

sudo pip install . --break-system-packages

cd ~/Avionics

#Install pyAvTools
git clone https://github.com/makerplane/pyAvTools.git
cd pyAvTools
sudo pip install . --break-system-packages

cd ~/Avionics

git clone https://github.com/btwatts/pyEfis.git
cd pyEfis
sudo pip install . --break-system-packages

cd ~/Avionics

# Get the CIFP Database
wget https://aeronav.faa.gov/Upload_313-d/cifp/CIFP_240125.zip
mkdir -p pyEfis/CIFP
unzip CIFP_240125.zip -d pyEfis/CIFP/

#tada, downloaded all the things!


**Using a Raspberry Pi 4B 2 Gig (or bigger)**

When using USB.  It is very important to use a USB 3.x device.  USB 2.x is too slow.
An SD card can be used if USB 3.x is not available but USB 3.x seems superior.


Install Raspberry Pi OS using Raspberry Pi Imager:  https://www.raspberrypi.com/software/

**Start Pi Imager**

Settings:
 * Raspberry Pi 4
 * Raspberry Pi OS (64-bit)
    - The version I am using most recently was:  Released 2024-10-22
 * USB Disk USB Device

 NEXT

  Would you like to apply OS customization settings?  (yes...)
  Edit Settings

    Set hostname:  ultra      .local
    Set username and password

        Username:  ultra
        Password:             something you can remember for now
    Configure wireless LAN
        SSID:    ... one that you have locally
        Password:    ... naturally so you can use ...it
    Wireless LAN country:  US
    Set locale settings
        Time zone:         America/Chicago
        Keyboard layout:   us

 SAVE
 YES

 All existing data on 'USB Disk USB Device' will be erased....

 YES

**Continue with Software Updates**

**OPTION TO USE DOCKER BEGIN**

# So many choices....this one (Version 1) appears to be the 'best'.

# Version 1 Begin   Ref:  https://raspberrytips.com/docker-on-raspberry-pi/

sudo apt update
sudo apt upgrade
sudo apt install ca-certificats curl
sudo curl -sSL https://get.docker.com | sh
sudo usermod -aG docker $USER
# Version 1 End

# Version 2 Begin   Ref:  https://www.xda-developers.com/how-to-install-docker-raspberry-pi/

# Remove old versions:
for pkg in docker.io docker-doc docker-compose podman-docker containerd runc do sudo apt remove $pkg; done

sudo apt update
sudo apt upgrade
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

#Add the repository to Apt sources:
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt upgrade (?)

sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

Note:  apparently docker-compose-plugin is no longer needed (comments in the ref article).

sudo usermod -aG docker $USER

# Version 2 End

# Once complete you can verify the installation was successful using the hello-world image:
Note:  You should not _need_ to use sudo since the $USER was added to the docker group

docker run hello-world

**OPTION TO USER DOCKER END**

...or...if not Docker


From a terminal (_in my case, I'm guessing there might also be a way to do this from the gui_):

sudo apt update
sudo apt upgrade
sudo apt autoclean
sudo apt autoremove

----------
After the update my system has Python 3.11.2 installed and ready to begin the installation of pyEfis
and supporting software.

**Update Splash Screens**

sudo cp new_splash.png /usr/share/plymouth/themes/pix/splash.png
sudo cp new_splash.jpg /usr/share/rpd-wallpaper/ultra_splash.png
sudo cp ultra_splash.jpg /usr/share/rpd-wallpaper/ultra_splash.jpg
sudo plymouth-set-default-theme -R pix

**Update Desktop Background Splash/Theme**
From the Pi configuration window right click on the screen background
* Desktop Preferences...
  - Picture:
    * ultra_splash.jpg
    Open
  OK
<!-- sudo pcmanfm --set-wallpaper /usr/share/rpd-wallpaper/ultra_splash.jpg -->

<!--
**-----  Install Python Qt6 / pyQt6  -----**
-->
<!--
**Note:  I'm beginning to wonder if switching to pyqt6 was wise.**

sudo apt install python3-full
<br/>
sudo apt install python3-pyqt6
-->
<!--
**-----  Set up [base] directory  -----**
-->
<!--
**--with virtual environment (optional)  -----**

**Note:**  This step might be causing problems later.

_working on it_...
-->
<!--
**mkdir Avionics**


**Note:**  Avionics is the [base] directory that I chose to use.  This could be any name.


**Note:**  [base] = Avionics in the following comments.
-->
<!--
**python -m venv Avionics**
<br/>
-->
<!--
**cd Avionics**
-->
<!--
<br/>
**source bin/activate**
-->
<!--
**TODO:  FIND OUT HOW TO AVOID --break-system-packages for installs**

**pipx** Ref: https://stackoverflow.com/questions/75608323/how-do-i-solve-error-externally-managed-environment-every-time-i-use-pip-3
-->

**Install pipx for github package installation**

apt install pipx
<!--
**-----  Install:  Python side stuff  -----**

**pip install wheel --break-system-packages**
<br/>
**pip install PyQt6 --break-system-packages**
-->

**-----  Install:  FIX-Gateway  -----**
<!--
From the [base] directory:
-->
<!--
~~git clone https://github.com/makerplane/FIX-Gateway.git~~

git clone https://github.com/btwatts/FIX-Gateway.git
-->
pipx install git+https://github.com/btwatts/FIX-Gateway.git

ln -s FIX-Gateway fixgw       this is an optional step
cd fixgw                      or                       cd FIX-Gateway
make venv
source venv/bin/activate
make init

<!--
**sudo python setup.py install**
-->
**sudo pip install . --break-system-packages**

Note:  Run FIX-Gateway can be run with:
       ./fixgw.py   or   python fixgw.py

<!--
       To-Do:  fixgw   should be able to run this, but currently does not
-->
**-----  Install:  pyAvTools  -----**

**Note:**  Install pyAvtools in the a peer directory to FIX-Gateway

cd .. (reset to [base] directory)

<!--
~~git clone https://github.com/makerplane/pyAvTools.git~~
git clone https://github.com/btwatts/pyAvTools.git
-->
pipx install git+https://github.com/btwatts/pyAvTools.git

cd pyAvTools
make venv
source venv/bin/activate
make init

<!--
sudo python setup.py install

**sudo pip install . --break-system-packages**
-->

**-----  Install:  pyEfis  -----**

**Note:**  Install pyEfis in the a peer directory to FIX-Gateway
<!--
cd ..  (reset to [base] directory)

git clone https://github.com/btwatts/pyEfis.git
-->
pipx install git+https://github.com/btwatts/pyEfis.git

cd pyEfis
make venv
source venv/bin/activate
make init

<!--
**sudo pip install --break-system-packages**
-->

**-----  Install CIFP FAA database  -----**


**Note:** It turns out that a search of "CIFP Download" brings this up in DuckDuck really quickly.
<br/>
What I've been doing is download the file (or files at the moment, because they have an update that is date specific due Jan 25, 2024).  Unpack the file to the pyEfis directory.  Then create a symbolic link in the pyEfis directory to the version of CIFP that I want to use.  Then run the code below to create the index file.
<p/>

Download the CIFP database from:  https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/cifp/download/ 
Unpack the zip file in:  pyEfis/CIFP
OR create a symbolic link (ln -s existing_directory CIFP) that results in the above directory.
<p/>
From the pyEfis/CIFP directory, run:
<br/>../../pyAvTools/MakeCIFPIndex.py FAACIFP18

**-----  Run FIX-Gateway  -----**<br/>
In one terminal window, run FIX-Gateway

cd FIX-Gateway

**./fixgw.py**   or   **python fixgw.py**

**-----  Run pyEfis  -----**<br/>
In a second terminal window, run pyEfis

cd ..  (reset to [base] directory)

**./pyEfis.py**   or   **python pyEfis.py**




-----
Summary of installed directories:
-----
<pre>
[base]/FIX-Gateway
[base]/pyAvTools
[base]/pyEfis
[base]/pyEfis/CIFP
</pre>

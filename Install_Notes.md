
**Using a Raspberry Pi 4B 2 Gig (or bigger)**

I also am using an SD card.  Raspberry Pi 4 and some others with updated firmware, can boot 
and run from USB but I am not pursuing that yet.

Download Raspberry Pi software distribution from:  https://www.raspberrypi.com/software/operating-systems/

I had trouble using imager_1.8.4.exe downloaded from https://www.raspberrypi.com/software/
So...I downloaded balenaEtcher-Setup-1.18.11.exe from https://etcher.balena.io/ https://etcher.balena.io/#download-etcher
which worked flawlessly.

**Install**

  **Note:**  I am currently using this one for my setup:

**2023-12-05-raspios-bookworm-arm64.img.xz**

or

**2023-12-05-raspios-bookworm-arm64-full.img.xz**

or a later version of something similar.

**Note:**  I had trouble setting up **2023-12-11-raspios-bookworm-arm64-lite.img.xz**, not
so much because I could not, but because it included a very limited set of packages and required
me to dig in and figure out what all needed to be installed....and configured.  I decided that I
am not desperate enough to drop that low on the software stack for now.

For whatever reason the install package configured everything except my WiFi which I did after I
chose to skip updates during install.  After reboot, finding my WiFi worked flawlessly.

From a terminal (_in my case, I'm guessing there might also be a way to do this from the gui_):

**sudo apt update**
<br/>
**sudo apt upgrade**
<br/>
**sudo apt autoremove**
<br/>
**sudo apt autoclean**

After the update my system has Python 3.11.2 installed and ready to begin the installation of pyEfis
and supporting software.


**-----  Install Python Qt6 / pyQt6  -----**

sudo apt install python3-full
<br/>
sudo apt install python3-pyqt6


**-----  Set up [base] directory  -----**
<!--
**--with virtual environment (optional)  -----**

**Note:**  This step might be causing problems later.

_working on it_...
-->

**mkdir Avionics**


**Note:**  Avionics is the [base] directory that I chose to use.  This could be any name.


**Note:**  [base] = Avionics in the following comments.

<!--
**python -m venv Avionics**
<br/>
-->
**cd Avionics**
<!--
<br/>
**source bin/activate**
-->

**-----  Install:  Python side stuff  -----**

**pip install wheel --break-system-packages**
<br/>
**pip install PyQt6 --break-system-packages**


**-----  Install:  FIX-Gateway  -----**

From the [base] directory:

git clone https://github.com/makerplane/FIX-Gateway.git

cd FIX-Gateway

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

git clone https://github.com/makerplane/pyAvTools.git

cd pyAvTools

<!--
sudo python setup.py install
-->
**sudo pip install . --break-system-packages**

**-----  Install:  pyEfis  -----**

**Note:**  Install pyEfis in the a peer directory to FIX-Gateway

cd ..  (reset to [base] directory)

git clone https://github.com/btwatts/pyEfis.git

cd pyEfis

**sudo pip install --break-system-packages**


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

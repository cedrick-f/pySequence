#Installation de pySéquence sous Ubuntu
**testé avec Ubuntu 14.04LT**

##Python 2.7##
déja installé
##wxPython 3##
http://wiki.wxpython.org/How%20to%20install%20wxPython#Installing_wxGTK_from_source
•	Télécharger : http://sourceforge.net/projects/wxpython/files/wxPython/3.0.2.0/wxPython-src-3.0.2.0.tar.bz2/download
•	depuis le dossier décompacté : wxPython-src-3.0.2.0
./configure --with-gtk


sudo apt-get install libgtk2.0-dev

./configure --with-gtk

make

sudo make install

sudo ldconfig

ça ne marche pas !

[http://wiki.wxpython.org/CheckInstall]
Checkinstall
sudo apt-get install checkinstall

Dépendances
sudo apt-get install dpkg-dev build-essential swig python2.7-dev libwebkitgtk-dev libjpeg-dev libtiff-dev checkinstall ubuntu-restricted-extras freeglut3 freeglut3-dev libgtk2.0-dev  libsdl1.2-dev libgstreamer-plugins-base0.10-dev 

Sources wxPython3.0
wget http://downloads.sourceforge.net/wxpython/wxPython-src-3.0.2.0.tar.bz2
tar xvjf wxPython-src-3.0.2.0.tar.bz2
cd wxPython-src-3.0.2.0/
mkdir bld
cd wxPython/

Compilation
sudo checkinstall -y --pkgname=wxpython --pkgversion=3.0.2 --pkgrelease=1 --pkglicense=wxWidgets --pkgsource=http://www.wxpython.org/ --maintainer=reingart@gmail.com --requires=python-wxversion,python2.7,python -D  python build-wxpython.py --build_dir=../bld --install

Test




##wxPython 2.8##
sudo apt-get install python-wxgtk2.8

##xlrd/xlwt##
sudo pip install xlrd
sudo pip install xlwt

##pyPdf2##
sudo pip install pypdf2

##pyperclip##
sudo pip install pyperclip

##enchant##
sudo pip install pyenchant






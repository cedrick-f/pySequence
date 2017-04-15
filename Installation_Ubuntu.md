# Installation de pySéquence sous Ubuntu #
pySéquence fonctionne sous Ubuntu avec les restrictions suivantes :
 * n'a pas encore été testé en profondeur : il y a sans doute pas mal de bugs
 * impossibilité de générer les grilles d'évaluation (elles sont au format Microsoft Excel, je n'y peux rien !)
 * des problèmes avec l'affichage des PDF
 * 

## Ubuntu 15.10 (et probablement les versions suivantes) ##

### pour utiliser pySéquence ###
```bash
sudo apt-get install python-pip

sudo apt-get install python-wxgtk3.0

sudo pip install pyenchant

sudo apt-get install python-reportlab

sudo pip install xhtml2pdf

sudo pip install xlrd

sudo pip install xlwt

sudo pip install comtypes

sudo pip install pyperclip
```

### pour générer un paquet .deb (je n'y arrive pas ! avis aux volontaires) ###
```bash
sudo apt-get install python-stdeb
```


## Ubuntu 14.04LT (ne fonctionne pas - adaptation non terminée) ##

##Python 2.7##
déja installé
##wxPython 3##
source : http://wiki.wxpython.org/CheckInstall
####Checkinstall####
```bash
sudo apt-get install checkinstall
```

####Dépendances####
```bash
sudo apt-get install dpkg-dev build-essential swig python2.7-dev libwebkitgtk-dev libjpeg-dev libtiff-dev checkinstall ubuntu-restricted-extras freeglut3 freeglut3-dev libgtk2.0-dev  libsdl1.2-dev libgstreamer-plugins-base0.10-dev 
```

####Sources wxPython3.0####
```bash
wget http://downloads.sourceforge.net/wxpython/wxPython-src-3.0.2.0.tar.bz2
tar xvjf wxPython-src-3.0.2.0.tar.bz2
cd wxPython-src-3.0.2.0/
mkdir bld
cd wxPython/
```

####Compilation####
```bash
sudo checkinstall -y --pkgname=wxpython --pkgversion=3.0.2 --pkgrelease=1 --pkglicense=wxWidgets --pkgsource=http://www.wxpython.org/ --maintainer=reingart@gmail.com --requires=python-wxversion,python2.7,python -D  python build-wxpython.py --build_dir=../bld --install
```

####Test####
```bash
python
```
```python
Python 2.7.3 (default, Sep 26 2012, 21:51:14) 
[GCC 4.7.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import wx
>>> wx.version()
'3.0.2.0 gtk2 (classic)'
```

Si ça ne fonctionne pas, utiliser wxpython2.8 ...




##wxPython 2.8##
```bash
sudo apt-get install python-wxgtk2.8
```

## pip ##
Outil d'installation de modules python

Installation : https://pip.pypa.io/en/stable/installing/

##xlrd/xlwt##
Modules de lecture/écriture de fichier Excel

source : https://pypi.python.org/pypi/xlrd
```bash
sudo pip install xlrd
```

source : https://pypi.python.org/pypi/xlwt
```bash
sudo pip install xlwt
```

##pyPdf2##
source : https://pypi.python.org/pypi/PyPDF2/1.25.1
```bash
sudo pip install pypdf2
```

##pyperclip##
Utilisation du clipboard (presse-papier)

source : https://pypi.python.org/pypi/pyperclip
```bash
sudo pip install pyperclip
```

##enchant##
Correcteur orthographique

source : https://pypi.python.org/pypi/pyenchant/
```bash
sudo pip install pyenchant
```

##xhtml2pdf##
Convertion html>pdf

source :  https://pypi.python.org/pypi/xhtml2pdf
```bash
sudo pip install xhtml2pdf
```

##markdown##
Générateur de texte Markdown

source :  https://pypi.python.org/pypi/Markdown
```bash
sudo pip install markdown
```


##pySéquence##
Télécharger une archive des sources de pySéquence : 

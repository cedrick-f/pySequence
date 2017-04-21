# Installation de pySéquence #
**avec Python 3**
en phase de test !!

_sous Windows, à partir des sources_


## Préparation ##
--------------

Désinstaller toute ancienne version de Python, ainsi que les modules.
Nettoyer le registre (ex CCleaner)

Package redistribuable Microsoft Visual C++ 2008 (x86)
https://www.microsoft.com/fr-FR/download/details.aspx?id=29

## Installations avec installeurs Windows ##
### Python ###
3.5 ou plus (mais pas Python 3 !)

https://www.python.org/downloads/



http://downloads.sourceforge.net/wxpython/wxPython3.0-win32-3.0.2.0-py27.exe

### pycairo ###

1.10.0

http://wxpython.org/cairo/py2cairo-1.10.0.win32-py2.7.exe

(en cas de problème, autre version : http://www.salsabeatmachine.org/python/pycairo-win32-packages.html)

Ajouter au PATH (variables d’environnement) :
 * C:\Python27\Lib\site-packages\wx-3.0-msw
 * C:\Python27\Lib\site-packages\wx-3.0-msw\wx

### pywin32 ###
220

https://sourceforge.net/projects/pywin32/files/pywin32/Build%20220/pywin32-220.win32-py2.7.exe/download





## Installations avec pip ##
-------------------------

Depuis une fenêtre de commande :

    cd c:\python27\scripts
    pip install --upgrade pip

### wxpython ###
4.0.0

    pip install wxpython
    
### cairocffi ###

    pip install cairocffi

### Beautifulsoup ###
4.4.1

    pip install beautifulsoup4
    
### markdown ###
    pip install markdown

### pyenchant ###
1.6.6

    pip install pyenchant

### reportlab (+ pillow) ###
3.3.0   -	3.2.0

    pip install reportlab

### xhtml2pdf 	(+ six, pyPdf2, html5lib) ###
0.0.6   -	 1.10.0 -    1.25.1-    1.0b8

    pip install xhtml2pdf
    pip install html5lib==1.0b8

### xlrd	xlwt ###
0.9.4   -	1.0.0

    pip install xlrd
    pip install xlwt

### comtypes ###
1.1.2

    pip install comtypes

### pyperclip ###
1.5.27

    pip install pyperclip



### rsvg (en cours de développement) ###
(source : https://github.com/jmcb/python-rsvg-dependencies)





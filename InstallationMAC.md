# Comment installer pySéquence sur un MAC ou sur Linux #

En principe, pySéquence est conçu pour être multi-plateforme.
En pratique, cela demande quelques adaptations ...

Encore jamais tentée jusqu'au bout, la procédure ci-dessous décrit donc pour l'instant la "théorie".
Au fur et à mesure de l'avancement de la procédure, cette page sera réactualisée. Merci donc d'avance aux possesseurs de MAC et Linux pour leurs retours d'expérience...

Cette procédure ne s'adresse donc qu'à des **utilisateurs confirmés** de MAC, prêts à passer un peu de **temps** à participer à cette adaptation.


## Installation de python et des modules nécessaires ##
  * Installer [python](http://www.python.org/), soit la [version 2.6](http://www.python.org/download/releases/2.6.6/), soit la [version 2.7](http://www.python.org/download/releases/2.7.6/).
  * [pyCairo](http://cairographics.org/download/) : suivre les instructions ...
  * [wxPython 3.0.1.1](http://wxpython.org/download.php#unstable) : choisir la version adaptée à la version de python installée.
  * [Reportlab](https://bitbucket.org/rptlab/reportlab) : tous les fichiers en téléchargement sont disponibles sur [cette page](http://www.reportlab.com/ftp/).
  * [pyPDF2](https://pypi.python.org/pypi/PyPDF2/1.18)
  * [xlrd](https://pypi.python.org/pypi/xlrd)
  * [xlwt](https://pypi.python.org/pypi/xlwt)
  * [beautifulsoup](http://www.crummy.com/software/BeautifulSoup/)

D'autres modules sont nécessaires ... mais sont spécifiques à Windows (utilisation de la base de registre, appels à Microsoft Excel, ...): il va donc y avoir quelques pertes de fonctionnalités.

## Installation de pySequence ##
Il faut utiliser directement les [sources](https://pysequence.googlecode.com/svn/branches).
L'idéal est d'utiliser svn, ce qui garantie d'avoir toujours la dernière version (prérelease) de pySequence.


## Lancement de pySequence ##
Il "suffit" de lancer le fichier src/sequence.py...

Il va immanquablement se produire plein d'erreurs !
Merci de [contacter les auteurs](Contact.md) pour qu'on règle ça.
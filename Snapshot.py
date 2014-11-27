#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                                    Snapshot                             ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2011 Cédrick FAURY

#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

# Programme de cr�ation d'un snapshot  de pyS�quence

#
import shutil
import os
import glob
import sys

PATH = os.path.dirname(os.path.abspath(sys.argv[0]))
#PATH = os.path.split(PATH)[0]
os.chdir(PATH)
sys.path.append(PATH)
print "Dossier de l'application :",PATH

DST = os.path.join(PATH, r"pySequence")

list_dir = [r"referentiels", r"tables", r"BO"]
for dir in list_dir:
    shutil.rmtree(os.path.join(DST, dir), ignore_errors=True)
    shutil.copytree(os.path.join(PATH, dir), os.path.join(DST, dir))

SRC = os.path.join(PATH, r"src")
BIN = os.path.join(DST, r"src")
shutil.rmtree(BIN, ignore_errors=True)
os.mkdir(BIN)
list_ext = [r"*.py", r"*.txt", r"*.ico"]

list_fich = []

for ext in list_ext:
    list_fich.extend(glob.glob(os.path.join(SRC, ext)))
          
                     
for fich in list_fich:
    shutil.copy2(os.path.join(SRC, fich), BIN)



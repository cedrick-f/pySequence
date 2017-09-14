#!/usr/bin/env python
# -*- coding: utf-8 -*-


##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                                   agenda                                ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2014 Cédrick FAURY - Jean-Claude FRICOU
##
## pySéquence : aide à la construction
## de Séquences et Progressions pédagogiques
## et à la validation de Projets

#    pySequence is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
    
#    pySequence is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with pySequence; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


u"""
module agenda
*************

Module.

"""


import sqlite3


def CreateTable(QueryCurs):
    QueryCurs.execute('''CREATE TABLE Clients
    (id INTEGER PRIMARY KEY, Nom TEXT,Rue TEXT,Ville TEXT, Region TEXT, Note REAL)''')

def AddEntry(QueryCurs, Nom,Rue,Ville,Region,Note):
    QueryCurs.execute('''INSERT INTO Clients (Nom,Rue,Ville,Region,Note)
    VALUES (?,?,?,?,?)''',(Nom,Rue,Ville,Region,Note))


if __name__ == '__main__':
    CreateDataBase = sqlite3.connect('MyDataBase.db')
    QueryCurs = CreateDataBase.cursor()
    
    
    CreateTable(QueryCurs)

    AddEntry(QueryCurs, 'Toto','Rue 1','Lille','Nord',105.2)
    AddEntry(QueryCurs, 'Bill','Rue 2','Fourmies','Nord',105.2)
    AddEntry(QueryCurs, 'Ben','Rue 3','Lille','Nord',105.2)
    AddEntry(QueryCurs, 'Paul','Rue 4','Lille','Nord',105.2)
    
    CreateDataBase.commit()

    QueryCurs.close()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                                   undo                                  ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2014 Cédrick FAURY - Jean-Claude FRICOU

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
module undo
***********

Gestion des actions annuler/rétablir

pySéquence : aide à la réalisation de fiches de séquence pédagogiques
et à la validation de projets

Copyright (C) 2015
@author: Cedrick FAURY

"""


TAILLE = 20

class UndoStack():
    def __init__(self, doc):
        self.doc = doc
        self.stack = []
        self.index = 1 # Le curseur qui point sur l'état "actuel" (en partant de la fin)
        self.onUndoRedo = False # Flag pour geler le "do" (True = pas de nouveau "do")


    def do(self, action):
        if not self.onUndoRedo:
            
            s = self.doc.getBranche()
            if self.index > 1:
                del self.stack[-self.index+1:]
                self.index = 1
            self.stack.append((s, action))
            del self.stack[:-TAILLE]
#            self.stack[min(self.getTaille(), TAILLE):] = [(s, action)]
            
#            print self.doc, ": do =", len(self.stack), self.index, action

    def undo(self):
        if self.index < TAILLE:
            self.index += 1
            self.doc.setBranche(self.stack[-self.index][0])
#            print self.doc, ": undo <<", len(self.stack), self.index, self.stack[-self.index][1]
            


    def redo(self):
        if self.index > 1:
            self.index -= 1
            self.doc.setBranche(self.stack[-self.index][0])
#            print self.doc, ": redo >>", len(self.stack), self.index, self.stack[-self.index][1]
            

    def setOnUndoRedo(self):
        self.onUndoRedo = True
        
    def resetOnUndoRedo(self):
        self.onUndoRedo = False


    def getUndoAction(self):
#        print self.getStack()
        if self.index < self.getTaille():
            return self.stack[-self.index][1]


    def getRedoAction(self):
#        print self.getStack()
        if self.index > 1:
            return self.stack[-self.index+1][1]

    def getStack(self):
        return [s[1] for s in self.stack]
    
    
    def getTaille(self):
        return len(self.stack)



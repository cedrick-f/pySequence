#!/usr/bin/env python
# -*- coding: utf-8 -*-


##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                                 pysequence                              ##
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


"""
module dpi_aware
****************
Pour obtenir un GUI au bon DPI pour écran haute résolution
"""


import ctypes, sys

# Sources :
# https://stackoverflow.com/questions/12471772/what-is-better-way-of-getting-windows-version-in-python
# https://stackoverflow.com/questions/44398075/can-dpi-scaling-be-enabled-disabled-programmatically-on-a-per-session-basis

def get_winver():
    wv = sys.getwindowsversion()
    if hasattr(wv, 'service_pack_major'):  # python >= 2.7
        sp = wv.service_pack_major or 0
    else:
        import re
        r = re.search("\s\d$", wv.service_pack)
        sp = int(r.group(0)) if r else 0
    return (wv.major, wv.minor, sp)

    
SSCALE = 1.0
def set_screen_scale():
    global SSCALE
    if not 'win' in sys.platform:
        return
    
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    
    WIN_8 = (6, 2, 0)
    WIN_7 = (6, 1, 0)
    WIN_SERVER_2008 = (6, 0, 1)
    WIN_VISTA_SP1 = (6, 0, 1)
    WIN_VISTA = (6, 0, 0)
    WIN_SERVER_2003_SP2 = (5, 2, 2)
    WIN_SERVER_2003_SP1 = (5, 2, 1)
    WIN_SERVER_2003 = (5, 2, 0)
    WIN_XP_SP3 = (5, 1, 3)
    WIN_XP_SP2 = (5, 1, 2)
    WIN_XP_SP1 = (5, 1, 1)
    WIN_XP = (5, 1, 0)
    
#     print "windows", get_winver()
    
    if get_winver() >= WIN_8:
        # Set DPI Awareness  (Windows 10 and 8)
        errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(2)
        # the argument is the awareness level, which can be 0, 1 or 2:
        # for 1-to-1 pixel control I seem to need it to be non-zero (I'm using level 2)
    elif get_winver() >= WIN_VISTA:
        # Set DPI Awareness  (Windows 7 and Vista)
        success = user32.SetProcessDPIAware()
        # behaviour on later OSes is undefined, although when I run it on my Windows 10 machine, it seems to work with effects identical to SetProcessDpiAwareness(1)


    screensize2 = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
#     print "screensize2", screensize2
    
    # Facteur d'échelle : 
    # tout ce qui est sensé être en PIXEL doit être multiplié par ce facteur
    SSCALE = 1.0*screensize2[0]/screensize[0]
    print(("Facteur d'echelle :", SSCALE))

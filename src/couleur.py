#!/usr/bin/env python
# -*- coding: utf-8 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                               draw_cairo_prg                            ##
##                                                                         ##
##                        Tracé des fiches de progression                  ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2011-2016 Cédrick FAURY

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

'''
code from :
http://www.eerock.com/blog/learn-python-color-gradient-generator/

choix des couleurs :
http://www.colorzilla.com/gradient-editor/
'''

import wx

# the baseline list of colors to generate the gradient from...
base_colors = [
    0xFFC3D6E5,
    0xFFEAA39D,
]


# get the number of colors to generate per step...
desired_gradient_length = 10



# color conversion utils
f2c = lambda f: int(f * 255.0) & 0xff
c2f = lambda c: float(c) / 255.0
alpha = lambda c: (c >> 24) & 0xff
red = lambda c: (c >> 16) & 0xff
green = lambda c: (c >> 8) & 0xff
blue = lambda c: c & 0xff
pack = lambda a, r, g, b: (f2c(a) << 24) | (f2c(r) << 16) | (f2c(g) << 8) | f2c(b)


# print the list of colors, easy to copy paste into the source code.
def print_results(colors):
    for c in colors:
        print('0x{0:x},'.format(c))


# run the generator and print the results to stdout.
def run():
    # generate the gradient
    grad = generate(base_colors, desired_gradient_length)

    # print the values to stdout, for ease of copy-paste.
#    print_results(grad)




# generate the gradient and returns the list of colors as packed ints.
def generate(gradient, base_colors, desired_gradient_length):
#    print "generate", base_colors, desired_gradient_length
    colors_per_step = max(2, 2*desired_gradient_length / len(base_colors))
    
    # get the 'corrected' length of the gradient...
    num_colors = int(colors_per_step) * len(base_colors)

    del gradient[:]
    for i, color in enumerate(base_colors[:-1]):
        # start color...
        r1 = c2f(red(color))
        g1 = c2f(green(color))
        b1 = c2f(blue(color))

        # end color...
        color2 = base_colors[(i + 1) % len(base_colors)]
        r2 = c2f(red(color2))
        g2 = c2f(green(color2))
        b2 = c2f(blue(color2))

        # generate a gradient of one step from color to color:
        delta = 1.0 / colors_per_step
        for j in range(int(colors_per_step)):
            t = j * delta
            a = 1.0
            r = (1.0 - t) * r1 + t * r2
            g = (1.0 - t) * g1 + t * g2
            b = (1.0 - t) * b1 + t * b2
#            print '   0x{0:x},'.format(pack(r, g, b, a))
#            gradient.append(pack(a, r, g, b))
            gradient.append((r, g, b, a))
    

def GetCouleurWx(C):
    if type(C) == str:
        return wx.NamedColour(C)
    else:
        return wx.Colour(C[0]*255, C[1]*255, C[2]*255)

def GetCouleurHTML(C):
    return GetCouleurWx(C).GetAsString(wx.C2S_CSS_SYNTAX)

def Couleur2Str(C):
    return ';'.join([str(c) for c in C])
    
def Str2Couleur(s):
    return tuple([float(c) for c in s.split(';')])

def Wx2Couleur(Wx):
    return (float(Wx.Red())/255, float(Wx.Green())/255, float(Wx.Blue())/255, float(Wx.Alpha())/255)

def Couleur2Wx(C):
    return wx.Colour(C[0]*255, C[1]*255, C[2]*255, C[3]*255)

# main entry point
if __name__ == '__main__':
    run()
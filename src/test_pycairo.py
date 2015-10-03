'''
Created on 3 oct. 2015

@author: Cedrick
'''
#! /usr/bin/env python
import cairo
from math import pi, sqrt

class Diagram(object):
    def __init__(self, filename, width, height):
        self.surface = cairo.SVGSurface(filename + '.svg', width, height)
        cr = self.cr = cairo.Context(self.surface)

        cr.scale(width, height)
        cr.set_line_width(0.01)

        cr.rectangle(0, 0, 1, 1)
        cr.set_source_rgb(1, 1, 1)
        cr.fill()

        self.draw_dest(cr)

        cr.set_line_width( max(cr.device_to_user_distance(2, 2)) )
        cr.set_source_rgb(0, 0, 0)
        cr.rectangle(0, 0, 1, 1)
        cr.stroke()

        self.surface.write_to_png(filename + '.png')
        cr.show_page()
        self.surface.finish()

class SetSourceRGBA(Diagram):
    def draw_dest(self, cr):
        cr.set_source_rgb(0, 0, 0)         #rgba
        cr.move_to(0, 0)                   #rgba
        cr.line_to(1, 1)                   #rgba
        cr.move_to(1, 0)                   #rgba
        cr.line_to(0, 1)                   #rgba
        cr.set_line_width(0.2)             #rgba
        cr.stroke()                        #rgba
                                           #rgba
        cr.rectangle(0, 0, 0.5, 0.5)       #rgba
        cr.set_source_rgba(1, 0, 0, 0.80)  #rgba
        cr.fill()                          #rgba
                                           #rgba
        cr.rectangle(0, 0.5, 0.5, 0.5)     #rgba
        cr.set_source_rgba(0, 1, 0, 0.60)  #rgba
        cr.fill()                          #rgba
                                           #rgba
        cr.rectangle(0.5, 0, 0.5, 0.5)     #rgba
        cr.set_source_rgba(0, 0, 1, 0.40)  #rgba
        cr.fill()                          #rgba

class SetSourceGradient(Diagram):
    def draw_dest(self, cr):
        radial = cairo.RadialGradient(0.25, 0.25, 0.1,  0.5, 0.5, 0.5) #gradient
        radial.add_color_stop_rgb(0,  1.0, 0.8, 0.8)                   #gradient
        radial.add_color_stop_rgb(1,  0.9, 0.0, 0.0)                   #gradient
                                                                       #gradient
        for i in range(1, 10):                                         #gradient
            for j in range(1, 10):                                     #gradient
                cr.rectangle(i/10.0 - 0.04, j/10.0 - 0.04, 0.08, 0.08) #gradient
        cr.set_source(radial)                                          #gradient
        cr.fill()                                                      #gradient
                                                                       #gradient
        linear = cairo.LinearGradient(0.25, 0.35, 0.75, 0.65)          #gradient
        linear.add_color_stop_rgba(0.00,  1, 1, 1, 0)                  #gradient
        linear.add_color_stop_rgba(0.25,  0, 1, 0, 0.5)                #gradient
        linear.add_color_stop_rgba(0.50,  1, 1, 1, 0)                  #gradient
        linear.add_color_stop_rgba(0.75,  0, 0, 1, 0.5)                #gradient
        linear.add_color_stop_rgba(1.00,  1, 1, 1, 0)                  #gradient
                                                                       #gradient
        cr.rectangle(0.0, 0.0, 1, 1)                                   #gradient
        cr.set_source(linear)                                          #gradient
        cr.fill()                                                      #gradient

class PathDiagram(Diagram):
    def draw_dest(self, cr):
        self.draw_dest_path(cr)

        path = list(cr.copy_path_flat())

        cr.set_line_width(max(cr.device_to_user_distance(3, 3)))
        cr.set_source_rgb(0, 0.6, 0)
        cr.stroke()

        if len(path) and path[-1][0] != cairo.PATH_CLOSE_PATH:
            x, y = path[0][1]
            cr.arc(x, y, max(cr.device_to_user_distance(5, 5)), 0, 2*pi)
            cr.set_source_rgba(0.0, 0.6, 0.0, 0.5)
            cr.fill()

            x, y = path[-1][1]
            cr.arc(x, y, max(cr.device_to_user_distance(5, 5)), 0, 2*pi)
            cr.set_source_rgba(0.0, 0.0, 0.75, 0.5)
            cr.fill()

class PathDiagramMoveTo(PathDiagram):
    def draw_dest_path(self, cr):
        cr.move_to(0.25, 0.25)                     #moveto

class PathDiagramLineTo(PathDiagramMoveTo):
    def draw_dest_path(self, cr):
        PathDiagramMoveTo.draw_dest_path(self, cr)
        cr.line_to(0.5, 0.375)                     #lineto
        cr.rel_line_to(0.25, -0.125)               #lineto

class PathDiagramArcTo(PathDiagramLineTo):
    def draw_dest_path(self, cr):
        PathDiagramLineTo.draw_dest_path(self, cr)
        cr.arc(0.5, 0.5, 0.25 * sqrt(2), -0.25 * pi, 0.25 * pi) #arc

class PathDiagramCurveTo(PathDiagramArcTo):
    def draw_dest_path(self, cr):
        if type(self) == PathDiagramCurveTo:
            cr.save()
            for x, y in ((0.5, 0.625), (0.5, 0.875)):
                cr.new_sub_path()
                cr.arc(x, y, max(cr.device_to_user_distance(3, 3)), 0, 2*pi)
                cr.set_source_rgba(0.5, 0, 0, 0.5)
                cr.fill()
            for (x, y, w, h) in ((0.25, 0.75, 0.25, 0.125),
                    (0.75, 0.75, -0.25, -0.125)):
                cr.move_to(x, y)
                cr.rel_line_to(w, h)
                cr.set_line_width(max(cr.device_to_user_distance(2, 2)))
                cr.set_source_rgba(0.5, 0, 0, 0.25)
                cr.stroke()
            cr.restore()
        PathDiagramArcTo.draw_dest_path(self, cr)
        cr.rel_curve_to(-0.25, -0.125, -0.25, 0.125, -0.5, 0)  #curveto

class PathDiagramClose(PathDiagramCurveTo):
    def draw_dest_path(self, cr):
        PathDiagramCurveTo.draw_dest_path(self, cr)
        cr.close_path()                                        #closepath

class TextExtents(Diagram):
    def draw_dest(self, cr):
        text = 'joy'
        cr.select_font_face('Georgia', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(0.5)
        px = max(cr.device_to_user_distance(1, 1))
        fascent, fdescent, fheight, fxadvance, fyadvance = cr.font_extents()
        xbearing, ybearing, width, height, xadvance, yadvance = \
                cr.text_extents(text)
        x = 0.5 - xbearing - width / 2
        y = 0.5 - fdescent + fheight / 2

        # baseline, descent, ascent, height
        cr.set_line_width(4 * px)
        cr.set_dash([9 * px], 0)
        cr.set_source_rgba(0, 0.6, 0, 0.5)
        cr.move_to(x + xbearing, y)
        cr.rel_line_to(width, 0)
        cr.move_to(x + xbearing, y + fdescent)
        cr.rel_line_to(width, 0)
        cr.move_to(x + xbearing, y - fascent)
        cr.rel_line_to(width, 0)
        cr.move_to(x + xbearing, y - fheight)
        cr.rel_line_to(width, 0)
        cr.stroke()

        # extents: width & height
        cr.set_source_rgba(0, 0, 0.75, 0.5)
        cr.set_line_width(1 * px)
        cr.set_dash([3 * px], 0)
        cr.rectangle(x + xbearing, y + ybearing, width, height)
        cr.stroke()

        # text
        cr.move_to(x, y)
        cr.set_source_rgb(0, 0, 0)
        cr.show_text(text)

        # bearing
        cr.set_dash([], 0)
        cr.set_line_width(2 * px)
        cr.set_source_rgba(0, 0, 0.75, 0.5)
        cr.move_to(x, y)
        cr.rel_line_to(xbearing, ybearing)
        cr.stroke()

        # text's advance
        cr.set_source_rgba(0, 0, 0.75, 0.5)
        cr.arc(x + xadvance, y + yadvance, 5 * px, 0, 2 * pi)
        cr.fill()

        # reference point
        cr.arc(x, y, 5 * px, 0, 2 * pi)
        cr.set_source_rgba(0.75, 0, 0, 0.5)
        cr.fill()


if __name__ == '__main__':
    size = 600
    SetSourceRGBA('setsourcergba', size, size)
    SetSourceGradient('setsourcegradient', size, size)
    PathDiagramMoveTo('path-moveto', size, size)
    PathDiagramLineTo('path-lineto', size, size)
    PathDiagramArcTo('path-arcto', size, size)
    PathDiagramCurveTo('path-curveto', size, size)
    PathDiagramClose('path-close', size, size)
    TextExtents('textextents', size, size)
    
    
    


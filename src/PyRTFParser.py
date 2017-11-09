# -*- coding: utf8 -*-
# Copyright (C) 2009-2010 The Board of Regents of the University of Wisconsin System
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of version 2 of the GNU General Public License as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#

""" An XML - RFT export / import Parser for the wxPython RichTextCtrl """

__author__ = 'David Woods <dwoods@wcer.wisc.edu>'
# Based on work by Donald N. Allingham and Gary Shao in 2000 and 2002 respectively
# Thanks to Tim Morton for help with output optimization

DEBUG = False   # Shows debug messages
DEBUG2 = True   # Shows unknown control words, not those explicitly ignored

# Transana is my program, and has some special requirements.  These can be skipped using this GLOBAL.
IN_TRANSANA = False

# Import wxPython and the wxPython wxRichTextCtrl
import wx
import wx.richtext as richtext

# import Python's cStringIO, os, and string modules
import cStringIO, os, string
# import Python's XML Sax handler
import xml.sax.handler
import struct


class PyRichTextRTFHandler(richtext.RichTextFileHandler):
    """ A RichTextFileHandler that can handle Rich Text Format files,
        at least to the extent that Transana needs Rich Text Format.
        by David K. Woods (dwoods@wcer.wisc.edu) """

    def __init__(self, name='RTF', ext='rtf'):
        """ Initialize the RichTextRTF Handler.
              Parameters:  name='RTF'
                           ext='rtf' """
        # Save the Handler Name
        self._name = name
        # Save the Handler Extension
        self._ext = ext

    def CanHandle(self, filename):
        """ Can this File Handler handle a particular file? """
        return os.path.splitext(filename)[1].lower() == ('.' + self._ext)

    def CanLoad(self):
        """ Can you load an RTF File with this handler? """
        return True

    def CanSave(self):
        """ Can you save an RTF File with this handler? """
        return True

    def DoLoadFile(self, buf, stream):
        return False

    def DoSaveFile(self, buf, stream):
        return False

    def GetEncoding(self):
        """ Get the encoding set for this handler """
        # NOTE:  I've only tried UTF8 encoding, which is currently hard-coded into the load and save classes.
        return 'utf8'

    def GetExtension(self):
        """ Get the handler file extension """
        return self._ext

    def GetName(self):
        """ Get the handler name """
        return self._name

    def GetType(self):
        """ Get the handler file type """
        return richtext.RICHTEXT_TYPE_RTF

    def IsVisible(self):
        return True

    def LoadFile(self, ctrl, filename):
        """ Load the contents of a Rich Text Format file into a wxRichTextCtrl.
            Parameters:  ctrl       a wxRichTextCtrl.  (NOT a wxRichTextBuffer.  The wxRichTextBuffer lacks methods for direct manipulation.)
                         filename   the name of the file to be loaded """
        if os.path.exists(filename) and isinstance(ctrl, richtext.RichTextCtrl):
            # Use the RTFToRichTextCtrlParser to handle the file load
            RTFTowxRichTextCtrlParser(ctrl, filename=filename, encoding=self.GetEncoding)
            # There's no feedback from the Parser, so we'll just assume things loaded.
            return True
        else:
            return False

    def LoadBuffer(self, ctrl, buf):
        """ Load the contents of a Rich Text Format file into a wxRichTextCtrl.
            Parameters:  ctrl       a wxRichTextCtrl.  (NOT a wxRichTextBuffer.  The wxRichTextBuffer lacks methods for direct manipulation.)
                         buf        the RTF string data to be loaded """
        if (len(buf) > 0) and isinstance(ctrl, richtext.RichTextCtrl):
            # Use the RTFToRichTextCtrlParser to handle the file load
            RTFTowxRichTextCtrlParser(ctrl, buf=buf, encoding=self.GetEncoding)
            # There's no feedback from the Parser, so we'll just assume things loaded.
            return True
        else:
            return False

    def SaveFile(self, buf, filename):
        """ Save the contents of a wxRichTextBuffer to a Rich Text Format file.
            Parameters:  buf       a wxRichTextBuffer or a wxRichTextCtrl
                         filename  the name of the file to be created or overwritten """
        # If we're passed a wxRichTextCtrl, we can get the control's buffer, which is what we need.
        if isinstance(buf, richtext.RichTextCtrl):
            buf = buf.GetBuffer()

        # Get a Rich Text XML Handler to extract the data from the wxRichTextBuffer in XML.
        # NOTE:  buf.Dump() just returns the text contents of the buffer, not any formatting information.
        xmlHandler = richtext.RichTextXMLHandler()
        # Create a stream object that can hold the data
        stream = cStringIO.StringIO()
        # Extract the wxRichTextBuffer data to the stream object
        if xmlHandler.SaveStream(buf, stream):
            # Convert the stream to a string
            contents = stream.getvalue()
            # Get the XML to RTF File Handler
            fileHandler = XMLToRTFHandler()
            # Use xml.sax, with the XML to RTF File Handler, to parse the XML and create
            # an RTF Output string.
            xml.sax.parseString(contents, fileHandler)
            # Use the XML to RTF File Handler to save the RTF Output String to a file
            fileHandler.saveFile(filename)
            # Assume success
            return True
        # If we couldn't extract the XML from the buffer ...
        else:
            # ... signal failure
            return False

    def SetName(self, name):
        """ Set the name of the File Handler """
        self._name = name


def IsHex(str):
    if str is None or len(str) == 0:
        return False
    str = str.upper()
    for i in str:
        if i not in string.hexdigits:
            return False
    return True


def utf8_to_enc(str):
    outstr = ""
    for i in str:
        c = repr(i.encode("gb2312"))[1:-1].replace("\\x", "")
        if IsHex(c) and len(c) == 4:
            outstr += struct.pack("2B", int(c[0:2], 16), int(c[2:4], 16))
        else:
            if c == "\\n":
                outstr += "\n"
            elif c == "\\\\":
                outstr += "\\"
            else:
                outstr += c
    return outstr


class XMLToRTFHandler(xml.sax.handler.ContentHandler):
    """ An xml.sax handler designed to convert wxRichTextCtrl's internal XML format data into
        Rich Text Format data that can be saved to *.rtf files, at least to the extent that
        Transana (htp://www.transana.org) needs Rich Text Format features supported.
        by David K. Woods (dwoods@wcer.wisc.edu) """

    def __init__(self, encoding='utf8'):
        """ Initialize the XMLToRTFHandler
            Parameters:  encoding='utf8'  Character Encoding to use (only utf8 has been tested, and I don't
                                          think the RTF Parser decodes yet. """
        # Remember the encoding to use
        self.encoding = encoding

        # Define an initial Fonts.  We define multiple levels of fonts to handle cascading styles.
        self.fontAttributes = {}
        self.fontAttributes[u'text'] = {u'bgcolor' : '#FFFFFF',
                                    u'fontface' : 'Courier New',
                                    u'fontsize' : 12,
                                    u'fontstyle' : wx.FONTSTYLE_NORMAL,
                                    u'fontunderlined' : u'0',
                                    u'fontweight' : wx.FONTSTYLE_NORMAL,
                                    u'textcolor' : '#000000'}

        self.fontAttributes[u'symbol'] = {u'bgcolor' : '#FFFFFF',
                                    u'fontface' : 'Courier New',
                                    u'fontsize' : 12,
                                    u'fontstyle' : wx.FONTSTYLE_NORMAL,
                                    u'fontunderlined' : u'0',
                                    u'fontweight' : wx.FONTSTYLE_NORMAL,
                                    u'textcolor' : '#000000'}

        self.fontAttributes[u'paragraph'] = {u'bgcolor' : '#FFFFFF',
                                         u'fontface' : 'Courier New',
                                         u'fontsize' : 12,
                                         u'fontstyle' : wx.FONTSTYLE_NORMAL,
                                         u'fontunderlined' : u'0',
                                         u'fontweight' : wx.FONTSTYLE_NORMAL,
                                         u'textcolor' : '#000000'}

        self.fontAttributes[u'paragraphlayout'] = {u'bgcolor' : '#FFFFFF',
                                               u'fontface' : 'Courier New',
                                               u'fontsize' : 12,
                                               u'fontstyle' : wx.FONTSTYLE_NORMAL,
                                               u'fontunderlined' : u'0',
                                               u'fontweight' : wx.FONTSTYLE_NORMAL,
                                               u'textcolor' : '#000000'}

        # Define the initial Paragraph attributes.  We define mulitple levels to handle cascading styles.
        self.paragraphAttributes = {}
        self.paragraphAttributes[u'paragraph'] = {u'alignment' : u'1',
                                                  u'linespacing' : u'10',
                                                  u'leftindent' : u'0',
                                                  u'rightindent' : u'0',
                                                  u'leftsubindent' : u'0',
                                                  u'parspacingbefore' : u'0',
                                                  u'parspacingafter' : u'0',
                                                  u'bulletnumber' : None,
                                                  u'bulletstyle' : None,
                                                  u'bulletfont' : None,
                                                  u'bulletsymbol' : None,
                                                  u'bullettext' : None,
                                                  u'tabs' : None}

        self.paragraphAttributes[u'paragraphlayout'] = {u'alignment' : u'1',
                                                      u'linespacing' : u'10',
                                                      u'leftindent' : u'0',
                                                      u'rightindent' : u'0',
                                                      u'leftsubindent' : u'0',
                                                      u'parspacingbefore' : u'0',
                                                      u'parspacingafter' : u'0',
                                                      u'bulletnumber' : None,
                                                      u'bulletstyle' : None,
                                                      u'bulletfont' : None,
                                                      u'bulletsymbol' : None,
                                                      u'bullettext' : None,
                                                      u'tabs' : None}

        # Define an initial font table
        self.fontTable = [u'Courier New']

        # define an initial color table
        self.colorTable = ['#000000', '#FF0000', '#00FF00', '#0000FF', '#FFFFFF']

        # Define the parsed text output  (cStringIO used for the speed improvements it provides!)
        self.outputString = cStringIO.StringIO()

        # Define a variable for tracking what element we are changing
        self.element = ''

        if IN_TRANSANA:
            # Track whether we're inside a Transana time code
            self.inTimeCode = False

        # Handling a URL
        self.url = ''

    def startElement(self, name, attributes):
        """ xml.sax required method for handling the starting XML element """

        # We need roman numerals for list processing
        # Copied from http://www.daniweb.com/code/snippet216865.html on 2/3/2010
        def int2roman(number):
            numerals = { 1 : "I", 4 : "IV", 5 : "V", 9 : "IX", 10 : "X", 40 : "XL",
                        50 : "L", 90 : "XC", 100 : "C", 400 : "CD", 500 : "D", 900 : "CM", 1000 : "M" }
            result = ""
            for value, numeral in sorted(numerals.items(), reverse=True):
                while number >= value:
                    result += numeral
                    number -= value
            return result

        # Remember the element's name
        self.element = name

        # If the element is a paragraphlayout, paragraph, symbol, or text element ...
        if name in [u'paragraphlayout', u'paragraph', u'symbol', u'text']:

            # Let's cascade the font and paragraph settings from a level up BEFORE we change things to reset the font and
            # paragraph settings to the proper initial state.  First, let's create empty character and paragraph cascade lists
            charcascade = paracascade = []
            # Initially, assume we will cascade from our current object for character styles
            cascadesource = name
            # If we're in a Paragraph spec ...
            if name == u'paragraph':
                # ... we need to cascase paragraph, symbol, and text styles for characters ...
                charcascade = [u'paragraph', u'symbol', u'text']
                # ... from the paragraph layout style for characters ...
                cascadesource = u'paragraphlayout'
                # ... and we need to cascare paragraph styles for paragraphs
                paracascade = [u'paragraph']
            # If we're in a Text spec ...
            elif name == u'text':
                # ... we need to cascase text styles for characters ...
                charcascade = [u'text']
                # ... from the paragraph style for characters ...
                cascadesource = u'paragraph'
            # If we're in a Symbol spec ...
            elif name == u'symbol':
                # ... we need to cascase symbol styles for characters ...
                charcascade = [u'symbol']
                # ... from the paragraph style for characters ...
                cascadesource = u'paragraph'
            # For each type of character style we need to cascade ...
            for x in charcascade:
                # ... iterate through the dictionary elements ...
                for y in self.fontAttributes[x].keys():
                    # ... and assign the character cascade source styles (cascadesource) to the destination element (x)
                    self.fontAttributes[x][y] = self.fontAttributes[cascadesource][y]
            # For each type of paragraph style we need to cascade ...
            for x in paracascade:
                # ... iterate through the dictionary elements ...
                for y in self.paragraphAttributes[x].keys():
                    # ... and assign the paragraph cascade source styles (cascadesource) to the destination element (x)
                    self.paragraphAttributes[x][y] = self.paragraphAttributes[cascadesource][y]

            # If the element is a paragraph element or a paragraph layout element, there is extra processing to do at the start
            if name in [u'paragraph', u'paragraphlayout']:
                # ... iterate through the element attributes looking for paragraph attributes
                for x in attributes.keys():
                    # If the attribute is a paragraph format attribute ...
                    if x in [u'alignment',
                             u'linespacing',
                             u'leftindent',
                             u'rightindent',
                             u'leftsubindent',
                             u'parspacingbefore',
                             u'parspacingafter',
                             u'bulletnumber',
                             u'bulletstyle',
                             u'bulletfont',
                             u'bulletsymbol',
                             u'bullettext',
                             u'tabs']:
                        # ... update the current paragraph dictionary
                        self.paragraphAttributes[name][x] = attributes[x]

            # ... iterate through the element attributes looking for font attributes
            for x in attributes.keys():
                # If the attribute is a font format attribute ...
                if x in [u'bgcolor',
                         u'fontface',
                         u'fontsize',
                         u'fontstyle',
                         u'fontunderlined',
                         u'fontweight',
                         u'textcolor']:
                    # ... update the current font dictionary
                    self.fontAttributes[name][x] = attributes[x]

                # If the attribute is a font name ...
                if x == u'fontface':
                    # ... that is not already in the font table ...
                    if not(attributes[x] in self.fontTable):
                        # ... add the font name to the font table list
                        self.fontTable.append(attributes[x])

                # If the element is a text element and the attribute is a url attribute ...
                if (name == u'text') and (x == u'url'):
                    # ... capture the URL data.
                    self.url = attributes[x]

            # Let's cascade the font and paragraph settings we've just changed.
            # First, let's create empty character and paragraph cascade lists
            charcascade = paracascade = []
            # Initially, assume we will cascade from our current object for character styles
            cascadesource = name
            # If we're in a Paragraph Layout spec ...
            if name == u'paragraphlayout':
                # ... we need to cascase paragraph, symbol, and text styles for characters ...
                charcascade = [u'paragraph', u'symbol', u'text']
                # ... we need to cascase paragraph styles for paragraphs ...
                paracascade = [u'paragraph']
            # If we're in a Paragraph spec ...
            elif name == u'paragraph':
                # ... we need to cascase symbol and text styles for characters ...
                charcascade = [u'symbol', u'text']
            # For each type of character style we need to cascade ...
            for x in charcascade:
                # ... iterate through the dictionary elements ...
                for y in self.fontAttributes[x].keys():
                    # ... and assign the character cascade source styles (cascadesource) to the destination element (x)
                    self.fontAttributes[x][y] = self.fontAttributes[cascadesource][y]
            for x in paracascade:
                # ... iterate through the dictionary elements ...
                for y in self.paragraphAttributes[x].keys():
                    # ... and assign the paragraph cascade source styles (cascadesource) to the destination element (x)
                    self.paragraphAttributes[x][y] = self.paragraphAttributes[cascadesource][y]

            if DEBUG:
                # List unknown elements
                for x in attributes.keys():
                    if not x in [u'bgcolor',
                                 u'fontface',
                                 u'fontsize',
                                 u'fontstyle',
                                 u'fontunderlined',
                                 u'fontweight',
                                 u'textcolor',
                                 u'alignment',
                                 u'linespacing',
                                 u'leftindent',
                                 u'rightindent',
                                 u'leftsubindent',
                                 u'parspacingbefore',
                                 u'parspacingafter',
                                 u'url',
                                 u'tabs',
                                 u'bulletnumber',
                                 u'bulletstyle',
                                 u'bulletfont',
                                 u'bulletsymbol',
                                 u'bullettext']:
                        print "Unknown %s attribute:  %s  %s" % (name, x, attributes[x])

        # If the element is an image element ...
        elif name in [u'image']:
            # ... if we have a PNG graphic ...
            if attributes[u'imagetype'] == u'15':  # wx.BITMAP_TYPE_PNG = 15
                # ... signal that we have a PNG image to process ...
                self.elementType = "ImagePNG"
                # ... and start the RTF code for a PNG image block
                self.outputString.write('{\pict\pngblip ')
            # It appears to me that all images will be PNG images coming from the RichTextCtrl.
            else:
                # if not, signal a unknown image type
                self.elementType = 'ImageUnknown'

                print "Image of UNKNOWN TYPE!!", attributes.keys()

        # If the element is a data or richtext element ...
        elif name in [u'data', u'richtext']:
            # ... we should do nothing here at this time
            pass
        # If we have an unhandled element ...
        else:
            # ... output a message and the element attributes.
            print "PyRTFParser.XMLToRTFHandler.startElement():  Unknown XML tag:", name
            for x in attributes.keys():
                print x, attributes[x]
            print

        # If the element is a paragraph element ...
        if name in [u'paragraph']:


            # Code for handling bullet lists and numbered lists is preliminary and probably very buggy

#            print "Bullet Number:", self.paragraphAttributes[u'paragraph'][u'bulletnumber'], type(self.paragraphAttributes[u'paragraph'][u'bulletnumber'])
#            print "Bullet Style:", self.paragraphAttributes[u'paragraph'][u'bulletstyle'],
#            if self.paragraphAttributes[u'paragraph'][u'bulletstyle'] != None:
#                print "%04x" % int(self.paragraphAttributes[u'paragraph'][u'bulletstyle'])
#            else:
#                print
#            print "Bullet Font:", self.paragraphAttributes[u'paragraph'][u'bulletfont']
#            print "Bullet Symbol:", self.paragraphAttributes[u'paragraph'][u'bulletsymbol']
#            print "Bullet Text:", self.paragraphAttributes[u'paragraph'][u'bullettext']
#            print

            # If we have a bullet or numbered list specification ...
            if self.paragraphAttributes[u'paragraph'][u'bulletstyle'] != None:
            # ... indicate that in the RTF output string
                self.outputString.write('{\\listtext\\pard\\plain')

                # Convert the Bullet Style to a hex string so we can interpret it correctly.
                # (I'm sure there's a better way to do this!)
                styleHexStr = "%04x" % int(self.paragraphAttributes[u'paragraph'][u'bulletstyle'])

                # If we have a known symbol bullet (TEXT_ATTR_BULLET_STYLE_SYMBOL and defined bulletsymbol) ...
                if (styleHexStr[2] == '2') and (self.paragraphAttributes[u'paragraph'][u'bulletsymbol'] != None):
                    # ... add that to the RTF Output String
                    try:
                        b = unichr(int(self.paragraphAttributes[u'paragraph'][u'bulletsymbol']))
                    except:
                        b = '*'
                        print "ERR", self.paragraphAttributes[u'paragraph'][u'bulletsymbol']
                    self.outputString.write("\\f%s %s\\tab}" % (self.fontTable.index(self.fontAttributes[name][u'fontface']), 
                                                                b))

                # if the second characters is a "2", we have richtext.TEXT_ATTR_BULLET_STYLE_STANDARD
                elif (styleHexStr[1] == '2'):
                    # If Symbol font is not yet in the Font Table ...
                    if not 'Symbol' in self.fontTable:
                        # ... then add it now.
                        self.fontTable.append('Symbol')
                    # add the bullet symbol in Symbol font to the RTF Output String
                    self.outputString.write("\\f%s \\'b7\\tab}" % self.fontTable.index('Symbol'))

                # If we have a know bullet NUMBER (i.e. a numbered list) ...
                elif self.paragraphAttributes[u'paragraph'][u'bulletnumber'] != None:
                    # Initialize variables used for presenting the proper "number" style and punctuation
                    numberChar = ''
                    numberLeadingChar = ''
                    numberTrailingChar = ''

                    # Put the bullet "number" into the correct format
                    # TEXT_ATTR_BULLET_STYLE_ARABIC
                    if styleHexStr[3] == '1':
                        numberChar = self.paragraphAttributes[u'paragraph'][u'bulletnumber']
                    # TEXT_ATTR_BULLET_STYLE_LETTERS_UPPER
                    elif styleHexStr[3] == '2':
                        bulletChars = string.uppercase[:26]
                        numberChar = bulletChars[int(self.paragraphAttributes[u'paragraph'][u'bulletnumber']) - 1]
                    # TEXT_ATTR_BULLET_STYLE_LETTERS_LOWER
                    elif styleHexStr[3] == '4':
                        bulletChars = string.lowercase[:26]
                        numberChar = bulletChars[int(self.paragraphAttributes[u'paragraph'][u'bulletnumber']) - 1]
                    # TEXT_ATTR_BULLET_STYLE_ROMAN_UPPER
                    elif styleHexStr[3] == '8':
                        numberChar = int2roman(int(self.paragraphAttributes[u'paragraph'][u'bulletnumber']))
                    # TEXT_ATTR_BULLET_STYLE_ROMAN_LOWER
                    elif styleHexStr[2] == '1':
                        numberChar = int2roman(int(self.paragraphAttributes[u'paragraph'][u'bulletnumber'])).lower()

                    # Put the bullet "number" into the correct punctuation structure
                    # TEXT_ATTR_BULLET_STYLE_PERIOD
                    if styleHexStr[1] == '1':
                        numberTrailingChar = '.'
                    # TEXT_ATTR_BULLET_STYLE_RIGHT_PARENTHESIS
                    elif styleHexStr[1] == '4':
                        numberTrailingChar = ')'
                    # TEXT_ATTR_BULLET_STYLE_PARENTHESIS
                    elif styleHexStr[2] == '8':
                        numberLeadingChar = '('
                        numberTrailingChar = ')'

                    # ... add that to the RTF Output String
                    self.outputString.write("\\f%s %s%s%s\\tab}" % (self.fontTable.index(self.fontAttributes[name][u'fontface']), numberLeadingChar, numberChar, numberTrailingChar))

                # If we have a know bullet symbol ...
                elif self.paragraphAttributes[u'paragraph'][u'bulletsymbol'] != None:
                    # ... add that to the RTF Output String
                    self.outputString.write("\\f%s %s\\tab}" % (self.fontTable.index(self.fontAttributes[name][u'fontface']), unichr(int(self.paragraphAttributes[u'paragraph'][u'bulletsymbol']))))

                # If we still don't know what kind of bullet we have, we're in trouble.
                else:
                    print "PyRTFParser.startElement() SYMBOL INSERTION FAILURE"

            # Signal the start of a new paragraph in the RTF output string
            self.outputString.write('\\pard')

            # Paragraph alignment left is u'1'
            if self.paragraphAttributes[u'paragraph'][u'alignment'] == u'1':
                self.outputString.write('\\ql')
            # Paragraph alignment centered is u'2'
            elif self.paragraphAttributes[u'paragraph'][u'alignment'] == u'2':
                self.outputString.write('\\qc')
            # Paragraph alignment right is u'3'
            elif self.paragraphAttributes[u'paragraph'][u'alignment'] == u'3':
                self.outputString.write('\\qr')
            else:
                print "Unknown alignment:", self.paragraphAttributes[u'paragraph'][u'alignment'], type(self.paragraphAttributes[u'paragraph'][u'alignment'])

            # line spacing u'10' is single line spacing, which is NOT included in the RTF as it is the default.
            if self.paragraphAttributes[u'paragraph'][u'linespacing'] == u'10':
                pass
            # 1.5 line spacing is u'15'
            elif self.paragraphAttributes[u'paragraph'][u'linespacing'] == u'15':
                # I'm not exactly sure why spacing for lines of 360, a multiple of normal, is the right specifier,
                # but that seems to be what Word uses.
                self.outputString.write('\\sl360\\slmult1')
            # double line spacing is u'20'
            elif self.paragraphAttributes[u'paragraph'][u'linespacing'] == u'20':
                # I'm not exactly sure why spacing for lines of 480, a multiple of normal, is the right specifier,
                # but that seems to be what Word uses.
                self.outputString.write('\\sl480\\slmult1')
            else:
                print "Unknown linespacing:", self.paragraphAttributes[u'paragraph'][u'linespacing'], type(self.paragraphAttributes[u'paragraph'][u'linespacing'])

            # Paragraph Margins and first-line indents
            # First, let's convert the unicode strings we got from the XML to integers and translate from wxRichTextCtrl's
            # system to RTF's system.
            # Left Indent in RTF is the sum of wxRichTextCtrl's left indent and left subindent
            leftindent = int(self.paragraphAttributes[u'paragraph'][u'leftindent']) + int(self.paragraphAttributes[u'paragraph'][u'leftsubindent'])
            # The First Line Indent in RTF is the wxRichTextCtrl's left indent minus the left indent calculated above.
            firstlineindent = int(self.paragraphAttributes[u'paragraph'][u'leftindent']) - leftindent
            # The Right Indent translates directly
            rightindent = int(self.paragraphAttributes[u'paragraph'][u'rightindent'])

            # Now let's convert what we got from the conversions above to twips.
            leftMargin = self.twips((leftindent) / 100.0)
            rightMargin = self.twips(rightindent / 100.0)
            firstIndent = self.twips((firstlineindent) / 100.0)
            # Now add these values to the RTF output string
            self.outputString.write('\\li%d\\ri%d\\fi%d' % (leftMargin, rightMargin, firstIndent))

            # Add non-zero Spacing before and after paragraphs to the RTF output String
            if int(self.paragraphAttributes[u'paragraph'][u'parspacingbefore']) != 0:
                self.outputString.write('\\sb%d' % self.twips(int(self.paragraphAttributes[u'paragraph'][u'parspacingbefore']) / 100.0))
            if int(self.paragraphAttributes[u'paragraph'][u'parspacingafter']) != 0:
                self.outputString.write('\\sa%d' % self.twips(int(self.paragraphAttributes[u'paragraph'][u'parspacingafter']) / 100.0))

            # If Tabs are defined ...
            if self.paragraphAttributes[u'paragraph'][u'tabs'] != None:
                # ... break the tab data into its component pieces
                tabStops = self.paragraphAttributes[u'paragraph'][u'tabs'].split(',')
                # For each tab stop ...
                for x in tabStops:
                    # ... (assuming the data isn't empty) ...
                    if x != u'':
                        # ... add the tab stop data to the RTF output string
                        self.outputString.write('\\tx%d' % self.twips(int(x) / 100.0))

        # Add Font formatting when we process text or symbol tags, as text and symbol specs can modify paragraph-level font specifications
        if name in [u'text', u'symbol']:
            # Begin an RTF block
            self.outputString.write('{')
            # Add Font Face information
            self.outputString.write('\\f%d' % self.fontTable.index(self.fontAttributes[name][u'fontface']))
            # Add Font Size information
            self.outputString.write('\\fs%d' % (int(self.fontAttributes[name][u'fontsize']) * 2))
            # If bold, add Bold
            if self.fontAttributes[name][u'fontweight'] == str(wx.FONTWEIGHT_BOLD):
                self.outputString.write('\\b')
            # If Italics, add Italics
            if self.fontAttributes[name][u'fontstyle'] == str(wx.FONTSTYLE_ITALIC):
                self.outputString.write('\\i')
            # If Underline, add Underline
            if self.fontAttributes[name][u'fontunderlined'] == u'1':
                self.outputString.write('\\ul')
            # If Text Color is not black ...
            if self.fontAttributes[name][u'textcolor'] != '#000000':
                # Check the color table.  If the color is not there ...
                if not self.fontAttributes[name][u'textcolor'] in self.colorTable:
                    # ... add it to the color table
                    self.colorTable.append(self.fontAttributes[name][u'textcolor'])
                # ... Add text foreground color
                self.outputString.write('\\cf%d' % self.colorTable.index(self.fontAttributes[name][u'textcolor']))
            # If Text Background Color is not White ...
            if self.fontAttributes[name][u'bgcolor'] != '#FFFFFF':
                # Check the color table.  If the color is not there ...
                if not self.fontAttributes[name][u'bgcolor'] in self.colorTable:
                    # ... add it to the color table
                    self.colorTable.append(self.fontAttributes[name][u'bgcolor'])
                # ... Add text background color to the RTF output string
                # Replaced "cb" with "highlight" for WORD compatibility.  "cb" works in OS X TextEdit.
                # self.outputString.write('\\cb%d' % self.colorTable.index(self.fontAttributes[name][u'bgcolor']))
                self.outputString.write('\\highlight%d' % self.colorTable.index(self.fontAttributes[name][u'bgcolor']))

            # Done with formatting string.  Add a space to terminate the formatting block, but don't close the text block yet.
            self.outputString.write(' ')


    def characters(self, data):
        """ xml.sax required method for handling the characters within XML elements """
        # If the characters come from a text element ...
        if self.element in ['text']:
            # Look for newline characters and replace them with the RTF-friendly '\line' specification.
            # (I don't think this line gets any hits.)
            data = data.replace('\n', '\\line')

            # If we have a value in self.URL, populated in startElement, ...
            if self.url != '':
                # ... then we're in the midst of a hyperlink.  Let's specify the URL for the RTF output string.
                self.outputString.write('{\\field{\\*\\fldinst HYPERLINK "%s"}{\\fldrslt ' % self.url)

            # If we have a single character in the data specification ...
            if len(data) == 1:
                # If we have an angle bracket (gt or lt) or a character above chr(127) ...
                if (data == '<') or (data == '>') or ord(data[0]) > 127:
                    # ... add the character NUMBER as a unicode character to the RTF.
                    # (NOTE:  This syntax is probably only correct under UTF8 encoding!)
                    self.outputString.write("\\u%d\\'3f" % ord(data[0]))
                # Otherwise, if we have something other than a quotation mark character ...
                elif data != '"':
                    # ... then add the encoded character to the RTF output string.  Since we're in the first 127 characters
                    # here, the encoding probably does nothing.
                    self.outputString.write(data.encode(self.encoding))

                # Transana requires special processing of Time Codes, with their "hidden" data
                if IN_TRANSANA:
                    # If we have a Transana Time Code character ...
                    if ord(data[0]) == 164:
                        # ... signal that we've started a time code and need to process the hidden data
                        self.inTimeCode = True
                    # If we are in a time code and hit the end of the data portion ...
                    elif self.inTimeCode and (data == '>'):
                        # ... signal that we're no longer in the time code ...
                        self.inTimeCode = False
                        # ... and add a space to finish the time code specification.
                        self.outputString.write(' ')

            # If we don't have a single character
            else:
                # If the text has leading or trailing spaces, it gets enclosed in quotation marks in the XML.
                # Otherwise, not.  We have to detect this and remove the quotes as needed.  Unicode characters
                # make this a bit more complicated, as in " 137 ë 137 ".
                if ((len(data) > 2) and ((data[0] == '"') or (data[-1] == '"')) and \
                    ((data[0] == ' ') or (data[1] == ' ') or (data[-2] == ' ') or (data[-1] == ' '))):
                    if data[0] == '"':
                        data = data[1:]
                    if data[-1] == '"':
                        data = data[:-1]
                # If we're in Transana, time code data if followed by a "(space)(quotationmark)" combination from the XML.
                # I'm not sure why, but this causes problems in the RTF.  Therefore skip this combo in Transana
                if not (IN_TRANSANA and (data == ' "')):
                    # Encode the data and add it to the RTF output string
                    self.outputString.write(data.encode(self.encoding))

            # If we've just added a URL hyperlink ...
            if self.url != '':
                # ... we need to close the link field RTF block
                self.outputString.write('}}')
                # Reset the URL to empty, as we're done with it.
                self.url = ''

        # If the characters come from a symbol element ...
        elif self.element == 'symbol':
            # Check that we don't have only whitespace, we don't have a multi-character string, and
            # we don't have a newline character.
            if (len(data.strip()) > 0) and ((len(data) != 1) or (ord(data) != 10)):
                # Convert the symbol data to the appropriate unicode character
                data = unichr(int(data))
                # Add that unicode character to the RTF output string
                self.outputString.write(data.encode(self.encoding))


        # If the characters come from a data element ...
        elif self.element == 'data':
            # If we're expecting a PNG Image ...
            if self.elementType == 'ImagePNG':
                # ... we can just add the data's data to the RTF output string
                self.outputString.write(data)
            # I haven't seen anything but PNG image data in this data structure from the RichTextCtrl's XML data
            else:
                # If we're dealing with an image, we could convert the image to PNG, then do a Hex conversion.
                # RTF can also JPEG images directly, as well as Enhanced Metafiles, Windows Metafiles, QuickDraw
                # pictures, none of which I think wxPython can handle.
                print "I don't know how to handle the data!!"

        # We can ignore whitespace here, which will be made up of the spaces added by XML and newline characters
        # that are part of the XML file but not part of the data.
        elif data.strip() != '':
            # Otherwise, print a message to the developer
            print "PyRTFParser.characters():  Unhandled text."
            print '"%s"' % data

    def endElement(self, name):
        """ xml.sax required method for handling the ending of an XML element (the close tag) """
        # If we have a text, data, or symbol end tag ...
        if name in [u'text', u'data', u'symbol']:
            # ... we need to close the RTF block
            self.outputString.write('}')
        # If we have a paragraph end tag ...
        elif name in [u'paragraph']:
            # ... we need to add the end paragraph RTF information
            self.outputString.write('\par\n')
        # If we have a text, data, paragraph, paragraphlayout, or richtext end tag ...
        if name in [u'text', u'data', u'paragraph', u'paragraphlayout', u'richtext']:
            # ... we need to clear the element type, as we're no longer processing that type of element!
            self.element = None

        # NOTE:  We could call "saveFile()" here with the richtext end tag (if we'd already gotten a file name.)
        # I decided not to do that, as there may be times when we want to get the RTF output string or a data
        # stream containing the RTF output stream rather than saving to a file.  I haven't written
        # getRTFString() or getStream() methods yet, but it wouldn't be hard.

    def saveFile(self, filename):
        """ Save the RTF Output String to a file """
        # Open the file for writing
        f = open(filename, 'w')

        # Add the appropriate RTF header information to the file.  This is VERY generic RTF information here.
        f.write('{\\rtf1\\ansi\\ansicpg1252\\deff0\n')

        # Write the Font Table information at the front of the file
        f.write('{\\fonttbl\n')
        # Iterate through the fontTable entries ...
        for x in range(len(self.fontTable)):
            # ... and add each font to the font table
            f.write('{\\f%d\\fmodern\\fcharset1\\fprq1 %s;}\n' % (x, utf8_to_enc(self.fontTable[x])))
        # Close the Font Table block
        f.write('}\n')

        # Write the Color Table information at the front of the file
        f.write('{\colortbl\n')
        # Iterate through the colorTable entries ...
        for x in range(len(self.colorTable)):
            # ... and add each color to the color table
            f.write('\\red%d\\green%d\\blue%d;' % (int(self.colorTable[x][1:3], 16), int(self.colorTable[x][3:5], 16), int(self.colorTable[x][5:7], 16)))
        # Close the Color Table block
        f.write('}\n')

        # Write the page definition information to the file.  This is VERY GENERIC information, and
        # probably should be converted to pull data from the default printer definition or something.
        # Start with no kerning, and a normal data view
        f.write('\\kerning0\\cf0\\viewkind1')
        # paper width of 8.5 inches (21.59 cm)
        f.write('\\paperw%d' % self.twips(21.59))
        # paper height of 11 inches (27.94 cm)
        f.write('\\paperh%d' % self.twips(27.94))
        # Margins of 1 inch (2.54 cm) all around
        f.write('\\margl%d' % self.twips(2.54))
        f.write('\\margr%d' % self.twips(2.54))
        f.write('\\margt%d' % self.twips(2.54))
        f.write('\\margb%d' % self.twips(2.54))
        # Specify widow/orphan control
        f.write('\\widowctrl\n')

        # now add the RTF output string from the XML parser
        f.write(self.outputString.getvalue())

        # Close the RTF document string
        f.write('}')
        # Close the output file
        f.close()

    def twips(self, cm):
        """ Convert centimeters to twips.  Twips are 1/72th of an inch, and are the official measurement unit of
            the RTF specification """
        return int(((cm/2.54)*72)+0.5)*20


class RTFTowxRichTextCtrlParser:
    """ An RTF Parser designed to convert Rich Text Format data from *.rtf files to
        wxRichTextCtrl's internal format, at least to the extent that
        Transana (htp://www.transana.org) needs Rich Text Format features supported.
        by David K. Woods (dwoods@wcer.wisc.edu) """

    def __init__(self, txtCtrl, filename=None, buf=None, encoding='utf8'):
        """ Initialize the RTFToRichTextCtrlParser.

            Parameters:  txtCtrl          a wx.RichTextCtrl, NOT a wx.RichTextBuffer.  The buffer doesn't provide an easy way to add text!
                         filename=None    a Rich Text Format (*.rtf) file name
                         buf=None         a string with RTF-encoded data
                         encoding='utf8'  Character Encoding to use (only utf8 has been tested, and I don't
                                          think the RTF Parser decodes yet.

            You can pass in either a filename or a buffer string.  If both are passed, only the file will be imported.  """

        # Remember the wxRichTextCtrl to populate
        self.txtCtrl = txtCtrl
        # At present, encoding is not used!
        self.encoding = encoding

        # Create a default font specification.  I've chosen Courier New, 12 point, black on white,
        self.font = {'fontfacename'  :  'Courier New',
                     'fontsize'      :  12,
                     'fontcolor'     :  wx.Colour(0, 0, 0),
                     'fontbgcolor'   :  wx.Colour(255, 255, 255)}

        # Create an object to hold font specifications for the current font
        self.txtAttr = richtext.RichTextAttr()
        # Apply the default font specifications to the current font object
        self.SetTxtStyle(fontFace = self.font['fontfacename'], fontSize = self.font['fontsize'],
                          fontColor = self.font['fontcolor'], fontBgColor = self.font['fontbgcolor'],
                          fontBold = False, fontItalic = False, fontUnderline = False)

        # If a file name was passed in and the file exists ...
        if (filename != None) and os.path.exists(filename):
            # ... open the file to be read ...
            f = open(filename, "r")
            # ... read its contents into a buffer ...
            self.buffer = f.read()
            # ... and close the file
            f.close()
        # If there's a buffer string passed in ...
        elif buf != None:
            self.buffer = buf
        # If there's nothing to read ...
        else:
            # ... create an empty buffer variable
            self.buffer = ''

        # Set the processing index to the start of the buffer
        self.index = 0

        # Initialize variables related to the Font Table
        self.in_font_table = False
        self.in_font_block = False
        self.fontName = ""
        self.fontNumber = -1
        self.fontTable = {}

        # Initialize the Default Font Number
        self.defaultFontNumber = 0

        # Initialize variables related to the Color Table
        self.in_color_table = False
        self.colorIndex = 0
        self.colorTable = [0x000000]

        # Initialize Paragraph settings
        self.paragraph = {'alignment'       : 'left',
                          'linespacing'     : richtext.TEXT_ATTR_LINE_SPACING_NORMAL,
                          'leftindent'      : 0,
                          'rightindent'     : 0,
                          'firstlineindent' : 0,
                          'spacingbefore'   : 0,
                          'spacingafter'    : 0,
                          'tabs'            : []}

        # Initialize variables related to processing images
        self.in_image = False
        self.image_type = None
        self.image_loaded = False

        # Initialize variables related to processing URLs
        self.in_field = 0
        self.in_url = False
        self.in_link = False
        self.url = ''

        # Initialize variables related to list processing
        self.in_list = False
        self.list_txt = ''

        # Initialize RTF block nesting counter
        self.nest = 0

        # Process the RTF document
        self.process_doc()

    def SetTxtStyle(self, fontColor = None, fontBgColor = None, fontFace = None, fontSize = None,
                          fontBold = None, fontItalic = None, fontUnderline = None,
                          parAlign = None, parLeftIndent = None, parRightIndent = None,
                          parTabs = None, parLineSpacing = None, parSpacingBefore = None, parSpacingAfter = None):
        """ I find some of the RichTextCtrl method names to be misleading.  Some character styles are stacked in the RichTextCtrl,
            and they are removed in the reverse order from how they are added, regardless of the method called.

            For example, starting with plain text, BeginBold() makes it bold, and BeginItalic() makes it bold-italic. EndBold()
            should make it italic but instead makes it bold. EndItalic() takes us back to plain text by removing the bold.

            According to Julian, this functions "as expected" because of the way the RichTextCtrl is written.

            The SetTxtStyle() method handles overlapping styles in a way that avoids this problem.  """

        # If the font face (font name) is specified, set the font face
        if fontFace:
            self.txtAttr.SetFontFaceName(fontFace)
            self.font['fontfacename'] = fontFace
        # If the font size is specified, set the font size
        if fontSize:
            self.txtAttr.SetFontSize(fontSize)
            self.font['fontsize'] = fontSize
        # If a color is specified, set text color
        if fontColor:
            self.txtAttr.SetTextColour(fontColor)
        # If a background color is specified, set the background color
        if fontBgColor:
            self.txtAttr.SetBackgroundColour(fontBgColor)
        # If bold is specified, set or remove bold as requested
        if fontBold != None:
            if fontBold:
                self.txtAttr.SetFontWeight(wx.FONTWEIGHT_BOLD)
            else:
                self.txtAttr.SetFontWeight(wx.FONTWEIGHT_NORMAL)
        # If italics is specified, set or remove bold as requested
        if fontItalic != None:
            if fontItalic:
                self.txtAttr.SetFontStyle(wx.FONTSTYLE_ITALIC)
            else:
                self.txtAttr.SetFontStyle(wx.FONTSTYLE_NORMAL)
        # If underline is specified, set or remove bold as requested
        if fontUnderline != None:
            if fontUnderline:
                self.txtAttr.SetFontUnderlined(True)
            else:
                self.txtAttr.SetFontUnderlined(False)
        # If Paragraph Alignment is specified, set the alignment
        if parAlign != None:
            self.txtAttr.SetAlignment(parAlign)
        # If Left Indent is specified, set the left indent
        if parLeftIndent != None:
            # Left Indent can be an integer for left margin only, or a 2-element tuple for left indent and left subindent.
            if type(parLeftIndent) == int:
                self.txtAttr.SetLeftIndent(parLeftIndent)
            elif (type(parLeftIndent) == tuple) and (len(parLeftIndent) > 1):
                self.txtAttr.SetLeftIndent(parLeftIndent[0], parLeftIndent[1])
        # If Right Indent is specified, set the right indent
        if parRightIndent != None:
            self.txtAttr.SetRightIndent(parRightIndent)
        # If Tabs are specified, set the tabs
        if parTabs != None:
            self.txtAttr.SetTabs(parTabs)
        # If Line Spacing is specified, set Line Spacing
        if parLineSpacing != None:
            self.txtAttr.SetLineSpacing(parLineSpacing)
        # If Paragraph Spacing Before is set, set spacing before
        if parSpacingBefore != None:
            self.txtAttr.SetParagraphSpacingBefore(parSpacingBefore)
        # If Paragraph Spacing After is set, set spacing after
        if parSpacingAfter != None:
            self.txtAttr.SetParagraphSpacingAfter(parSpacingAfter)
        # Apply the modified font to the document
        self.txtCtrl.SetDefaultStyle(self.txtAttr)

    def process_doc(self):
        """ Process and parse a document in Rich Text Format """
        # Initialize a text variable
        txt = ""

        # We need to go through the file buffer one character at a time
        while self.index < len(self.buffer):
            # Get one character
            c = self.buffer[self.index]

            # Handle curly brackets and backslash characters
            if "{}\\".count(c) > 0:

                # Open curly bracket starts an RTF text block
                if (c == '{'):
                    # Reset Default Font
                    self.SetTxtStyle(fontFace = self.font['fontfacename'], fontSize = self.font['fontsize'],
                                      fontColor = self.font['fontcolor'], fontBgColor = self.font['fontbgcolor'],
                                      fontBold = False, fontItalic = False, fontUnderline = False)

                # If the characters are preceded by a backslash, skip that backslash character
                if self.buffer[self.index : self.index + 2] in ['\{', '\}', '\\\\']:
                    # Add only the second character to the local text variable
                    txt += self.buffer[self.index + 1]
                    # Move the index past both characters
                    self.index += 2

                # See if we have a WORD-style Unicode character specifier, (backslash)(apostrophe) ...
                elif (self.buffer[self.index : self.index+2] in ["\\'", "\\\'"]):
                    # The WORD style is \'hh, where hh is a hex representation of the character.
                    # Get the hex part and convert it to an integer value.
                    val = int(self.buffer[self.index+2:self.index+4], 16)

                    # Word Smart Quotes cause problems.  These come across as "\'93" and "\'94"
                    #(hex for 147 and 148) and need to be replaced with a normal quote character.
                    if (val in [147, 148]):
                        # 22 is the HEX value for chr(34), the quotation mark character.
                        val = 34
                        # Replace smart quote with regular quotes in the self.buffer text.
                        self.buffer = self.buffer[:self.index+2] + '22' + self.buffer[self.index+4:]

                    # If there's text in the buffer when we do this ...   (There never should be text here, but no harm done.)
                    if txt != '':
                        # ... we need to process that text before going any further
                        self.process_text(txt)
                        # and now that the text is processed, we need to clear it from the local text variable.
                        txt = ''

                    # If we encounter Unicode characters while naming a font ...
                    if self.in_font_block:
                        # If our character value is 161 or larger ...
                        if val >= 161:
                            # ... we can add the appropriate unicode character to the font name
                            txt += unichr(val)
                        # If our value is less than 161 ...
                        elif val > 138:
                            # ... then unichr() and chr() disagree, and we need the chr() character instead.
                            txt += chr(val)
                    else:
                        # If our character value is 161 or larger ...
                        if val >= 161:
                            # ... we can insert the appropriate unicode character
                            self.process_text(unichr(val))
                        # If our value is less than 161 ...
                        elif val > 138:
                            # ... then unichr() and chr() disagree, and we need the chr() character instead.
                            self.process_text(chr(val))

                    # We are now done inserting the character, so can move 4 positions in the buffer to get past it.
                    self.index += 4

                # If we're not dealing with an escaped character, continue normal processing
                else:
                    # If we're in a Font block within the Font Table ...
                    if self.in_font_block and len(txt) > 0:
                        # If the txt is not blank ...
                        if txt[:-1] != '':
                            # ... it must be the font name!  Grab it!
                            self.fontName = txt[:-1]
                        # Clear the txt, since we've used it
                        txt = ""
                        # Add the font number / name combination to the Font Table
                        self.fontTable[self.fontNumber] = self.fontName

                    # If we're in a list and txt has been captured ...
                    elif self.in_list and len(txt) > 0:
                        # ... we need to store it for later, after more formatting is determined ...
                        self.list_txt += txt
                        # ... and we need to blank out txt.
                        txt = ''

                    # If we are NOT in an image or in a URL field ...
                    elif (not self.in_image) and (not self.in_field):
                        # ... then we should process the text
                        self.process_text(txt)
                        # Clear the txt, since we've used it
                        txt = ""

                    # If our character opens an RTF block ...
                    if c == '{':
                        # ... note one level deeper in block nesting
                        self.nest += 1
                        # If we're in the font table ...
                        if (self.in_font_table):
                            # ... then we are entering a font block ...
                            self.in_font_block = True
                        # ... and we can move on to the next character
                        self.index += 1

                    # If our character closes an RTF block ...
                    elif c == '}':
                        # ... note one less deep in the block nesting
                        self.nest -= 1

                        # If we're in a font block ...
                        if (self.in_font_block):
                            # ... this signals we're leaving the font block
                            self.in_font_block = False
                            # ... and we can move on to the next character
                            self.index += 1

                        # If we're in the font table but NOT in a font block ...
                        elif (self.in_font_table) or (self.in_list):
                            # ... we can end the font table block
                            self.process_end_block()

                        # If we're in an image ...
                        elif self.in_image:
                            # If there's data in the local text variable ...
                            if txt != '':
                                # ... and that data STARTS with an asterisk ...
                                if txt[0] != '*':
                                    # ... if we have a PNG (implemented, tested) or a JPEG (not implemented not tested, theoretically possible) ...
                                    if self.image_type in [wx.BITMAP_TYPE_PNG, wx.BITMAP_TYPE_JPEG]:
                                        # Create a StringIO stream from the HEX-converted image data
                                        stream = cStringIO.StringIO(self.hex2int(txt))
                                        # Now convert that stream to an image
                                        img = wx.ImageFromStream(stream, self.image_type)
                                        # If we were successful in creating a valid image ...
                                        if img.IsOk():
                                            # ... add that image to the wxRichTextEdit control
                                            self.txtCtrl.WriteImage(img)
                                        # Whether successful or not, signal that our load attempt is completed.
                                        self.image_loaded = True
                                    # ... if we have a Windows Metafile image ...
                                    elif self.image_type == 'WMETAFILE':
                                        # ... if the image isn't already loaded through the PNG alternate method ...
                                        if not self.image_loaded:
                                            # ... then indicate our inability to convert this type of image using text in the wxRichTextCtrl
                                            self.txtCtrl.WriteText(' (Unable to convert Windows Metafile image data.) ')
                                    # ... if we have a MacPict (QuickDraw?) image ...
                                    elif self.image_type == 'MACPICT':
                                        # ... if the image isn't already loaded through the PNG alternate method ...
                                        if not self.image_loaded:
                                            # ... then indicate our inability to convert this type of image using text in the wxRichTextCtrl
                                            self.txtCtrl.WriteText(' (Unable to convert Macintosh image data.) ')
                                    # ... if we have an unknown image type ...
                                    else:
                                        # ... if the image isn't already loaded through the PNG alternate method ...
                                        if not self.image_loaded:
                                            # ... then indicate our inability to convert this type of image using text in the wxRichTextCtrl
                                            self.txtCtrl.WriteText(' (Unable to convert image data.) ')
                            # Now that we've used the image data, we can clear the local text variable ...
                            txt = ""
                            # ... and we need to process the end of the block
                            self.process_end_block()

                        # ... if we're in a URL / Hyperlink field ...
                        elif self.in_field > 0:
                            # If we're expecting the URL to come next ...
                            if self.in_url:
                                # ... check for the HYPERLINK keyword ...
                                if txt[:10] == 'HYPERLINK ':
                                    # ... and capture the data (without the keyword) as the URL
                                    self.url = txt[11:]
                                # If we were expecting a URL, we no longer are, even if we didn't get one.
                                self.in_url = False
                                # Move on to the next character, but don't close the block yet.
                                self.index += 1
                            # If we're expecting the LINK text ...
                            elif self.in_link:
                                # ... and we have a URL ...
                                if self.url != '':
                                    # ... then create a URL style for the text
                                    urlStyle = richtext.RichTextAttr()
                                    urlStyle.SetFontFaceName(self.font['fontfacename'])
                                    urlStyle.SetFontSize(self.font['fontsize'])
                                    urlStyle.SetTextColour(wx.BLUE)
                                    urlStyle.SetFontUnderlined(True)
                                    # Apply the URL style
                                    self.txtCtrl.BeginStyle(urlStyle)
                                    # Add the URL value itself
                                    self.txtCtrl.BeginURL(self.url)
                                    # Add the link text
                                    self.txtCtrl.WriteText(txt)
                                    # End the URL
                                    self.txtCtrl.EndURL()
                                    # End the URL style
                                    self.txtCtrl.EndStyle()
                                # If we don't have a URL ...
                                else:
                                    # ... something's wrong, but put the link text here anyway, with no actual hyperlink
                                    self.txtCtrl.WriteText(txt)
                                # Now we can process the end of the URL field block
                                self.process_end_block()
                            # If we're expecting neither a URL or the LINK text ...
                            else:
                                # ... we can just move on to the next character
                                self.index += 1
                            # Clear the local text variable
                            txt = ""
                        # If we're closing a block but don't need to do any of the specific processing above ...
                        else:
                            # Just close the block.  (This probably does little more than move to the next character
                            self.process_end_block()

                    # If we have a backslash character ...
                    elif c == '\\':
                        # ... that signals the START of a control word we should process
                        self.process_control_word()

                    # If we don't have any of those special characters ... (SHOULD NEVER BE FIRED!)
                    else:
                        # ... just move on to the next character
                        self.index += 1

            # If we don't have a special character (\\, { or }) to process ...
            else:
                # If we're in the color table and have a semicolon character ...
                if (self.in_color_table) and (c == ";"):
                    # ... then increment the color index to the next color
                    self.colorIndex += 1
                # For any other character other than a newline or \r ...
                elif (c != '\r' and c != '\n'):
                    # ... add the character to the local text variable ...
                    txt = txt + c
                # ... and move on to the next character
                self.index += 1

    def hex2int(self, data):
        """ Image data is stored in a file-friendly Hex format.  We need to convert it to an image-friendly binary format. """
        # Initialize the conversion result variable
        result = ''
        # For each PAIR of characters in the hex data string ...
        for x in range(0, len(data), 2):
            # ... convert the hex pair into a integer, find that character, and add it to the result variable
            result += chr(int(data[x : x + 2], 16))
        # Return the converted data
        return result

    def process_text(self, txt):
        """ Process a text string """
        
##        # Please ignore this commented code.  It's stuff I might need to resurrect for Transana, but might not.
##        if len(txt) > 0:
##        # Since timecode, and up/down intonation symbols are different between
##        # OSX and windows, we need to perform substitution while loading a document.
##        if ('unicode' in wx.PlatformInfo) and ('wxMac' in wx.PlatformInfo):
##
##                if DEBUG:
##                    print "RTFParser.process_text(): '%s' .. " % txt,
##                    for x in txt:
##                        print ord(x),
##                    print
##
##        # This (array.array('B', txt).tolist()) is supposed to be the most efficient way
##        # of converting a string to a list of integers.  JB
##        # Unfortunately, it requires a string, not a Unicode object.  We'll need a less
##        # efficient alternative for Unicode.  DKW
##
##                # Check the type of the txt object.  If it's a string ...
##        if isinstance(txt, str):
##                    # ... convert it efficiently to a list of integers
##                    intList = array.array('B', txt).tolist()
##                # If txt is Unicode ...
##                else:
##                    # ... create an empty list ...
##                    intList = []
##                    # ... iterate through the characters in the Unicode string ...
##                    for x in txt:
##                        # ... and add the integer value for each character to the integer list
##                        intList.append(ord(x))
##
##        try:
##            # all the windows special characters begin with \xc2 (#194)
##            position = intList.index(194)
##
##            # test for timecode
### It appears that with wxPython 2.8.0.1, the Mac can now handle the proper timecode character!
###            if intList[position+1] == 164:
##
###            if DEBUG:
###                print "RTFParser.process_text():  Mac Unicode Substitution - Time Code."
##
###            newString = txt[0:position] + unicode('\xc2\xa7', 'utf8')
###            txt = newString
##            # Test for up intonation
###            elif intList[position+1] == 173:
##            if intList[position+1] == 173:
##            if DEBUG:
##                print "RTFParser.process_text(): Mac Unicode Substitution - Up Arrow."
##
##            newString = txt[0:position] + unicode('\xe2\x89\xa0', 'utf8')
##            txt = newString
##            # Test for down intonation
##            elif intList[position+1] == 175:
##
##            if DEBUG:
##                print "RTFParser.process_text(): Mac Unicode Substitution - Down Arrow."
##
##            newString = txt[0:position] + unicode('\xc3\x98', 'utf8')
##            txt = newString
##            # Test for closed dot (hi dot)  (194 149 is 1.24 encoding, 194 183 is 2.05 encoding)
##            # but the 2.05 encoding doesn't work here because we don't want the text to be in Symbol font.
##            # That is handled in RichTextEditCtrl.py's __ParseRTFText() method.
##            elif (intList[position+1] == 149):
##
##            if DEBUG:
##                print "RTFParser.process_text(): Mac Unicode Substitution - closed dot."
##
##            newString = unicode('\xe2\x80\xa2', 'utf8')  # txt[0:position] + unicode('\xe2\x80\xa2', 'utf8')
##            txt = newString
##            # DON'T Test for open dot (whisper)  (194 176 is 2.05 encoding)
##            # but the 2.05 encoding doesn't work here because we don't want the text to be in Symbol font.
##            # That is handled in RichTextEditCtrl.py's __ParseRTFText() method.
##
##        except ValueError:
##            i = 1
##
##        do = DocObject()
##          do.text = txt
##          self.stream.append(do)

        # If data is passed in (txt is sometimes empty!) ...
        if txt != "":
            # If we've been gathering list text before now ...
            if (len(self.list_txt) > 0):
                # ... then it's now time to insert the list text in front of the new text.
                # That is, we finally have all the list formatting in place.
                self.txtCtrl.WriteText(self.list_txt + txt)
                # Clear the list text
                self.list_txt = ''
            else:
                # ... then add that text to the wxRichTextCtrl.
                # NOTE:  I don't appear to need to decode things here.  I think RTF takes care of that in the way it
                #        encodes Unicode characters.  If you run into encoding problems, try determing self.encoding from
                #        the RTF file (maybe the ansicpg in the rtf header) and use txt.decode(self.encoding).
                self.txtCtrl.WriteText(txt)

    def process_control_word(self):
        """ Process a Rich Text Format control word """
        # The \ character signals an RTF Control Word.  Confirm that.
        if self.buffer[self.index] != "\\":
            # Raise an exception if we don't have a backslash!
            raise RTFParseError, "Expected \\ (programming error?)"

        # Start exception handling
        try:
            # Initialize the ControlWord variable
            cw = ""
            # Move to the first character following the backslash
            self.index += 1
            # Get the character to process
            c = self.buffer[self.index]
            # As long as we are processing LETTERS ...
            while string.ascii_letters.count(c) > 0:
                # ... add the character to the control word ...
                cw = cw + c
                # ... increment the index ...
                self.index += 1
                # ... and look at the next character
                c = self.buffer[self.index]

            # Now index is at the first character after the control word, which might be a number that modifies the control word.
            # As long as we are processing NUMBERS or the minus sign ...
            if (string.digits.count(c) > 0 or (c == '-')):
                # Start collecting digits.  (This structure means only the first character can be the minus sign.)
                numstr = c
                # Increment the index ...
                self.index += 1
                # ... and look for the next digit
                c = self.buffer[self.index]
                # From now on, we only want digits ...
                while string.digits.count(c) > 0:
                    # ... add the next digit to the number string ...
                    numstr += c
                    # ... increment the index ...
                    self.index += 1
                    # ... and look for the next digit
                    c = self.buffer[self.index]
                # Start exception handling
                try:
                    # Convert the number string to an integer
                    num = int(numstr)
                # If the conversion raises an exception ...
                except:
                    # ... then we don't really have a number.
                    num = 0
            # If the next character was not a number ...
            else:
                # ... we need to at least initialize the num variable
                num = None

            if DEBUG:
                print "Processing control word '%s' with numeric parameter %s" % (cw, num)

            # Now index points to the first non-digit character after the control word.
            # If the next character is a space ...
            if (c == ' '):
                # skip the space.  Spaces here are considered to be the control word's terminator
                # and are not real text that should be processed.
                self.index += 1

            # If c is an asterisk and we have a blank control word, we're pointing at a "\*", which is a special
            # case in Rich Text Format.  This is often data that can be ignored as redundant, but there are a few
            # special cases where we need that data.
            if (c == '*' and cw == ''):

                # If \* is followed by \shppict or \picprop,
                # or if we are in a field and are looking at a \fldinst control word, we need to keep processing
                if (self.buffer[self.index + 1 : self.index + 9] == '\\shppict') or \
                   (self.buffer[self.index + 1 : self.index + 9] == '\\picprop') or \
                   ((self.in_field) and (self.buffer[self.index + 1 : self.index + 9] == '\\fldinst')):
                    # in order to not skip the following RTF control words, set the Control Word to * ...
                    cw = '*'
                    # ... and increment the index
                    self.index += 1
                    # We're done here.
                    return
                # If we have \* followed by anything else ...
                else:
                    # This is a special case I haven't completely figured out yet.
                    # For now we assume that any block that has a \* in it
                    # is a block containing user property definitions that we
                    # don't care about, so we jump to the end of the block.
                    self.seek_eob()
                    # We're done here.
                    return

##            # Again, we have a block of code I might still need for Transana, so don't want to remove just yet.  Please ignore it.
##            if (c == "'" and cw == ''):
##                # \'hh is a hex value for the current charset
##                self.index += 1
##                try:
##                    value = int(self.buf[self.index:self.index+2], 16)
##
##                    if DEBUG:
##                        print "RTFParser.process_control_word()", self.buf[self.index:self.index+2], "value =", value
##
##                    if ('unicode' in wx.PlatformInfo):
##                        # Try a straight conversion to UTF-8, the DefaultPyEncoding
##                        try:
##                            # CHANGED for 2.30 because 201 is now the back-accented capital E character!
##                            if value == 133:  # 201
##
##                                if DEBUG:
##                                    print "Elipsis substitution"
##
##                                self.process_text('...')
##                            else:
##                                tempChar = unichr(value)
##                                # I'm not sure why passing through latin-1 is needed, but it appears to be necessary.
##                                # tempChar = unicode(chr(value), 'latin-1')
##                                self.process_text(tempChar.encode(TransanaGlobal.encoding))
##
##                        except UnicodeEncodeError:
##                            # If we get a UnicodeEncodeError, as we do for Time Codes, let's try going through
##                            # Latin-1 encoding to translate the single-byte character into a 2-byte character.
##                            # The default encoding for RTF is Transana at least if ansicpg1252, which I think
##                            # is equivalent to Latin-1
##                            tempc = unicode(chr(value), 'latin1')
##
##                            if DEBUG:
##                                print "Passing through Latin-1"
##
##                            self.process_text(tempc.encode(TransanaGlobal.encoding))
##
##                            if DEBUG:
##                                print "Should now be encoded as %s" % TransanaGlobal.encoding
##
##                    else:
##                        self.process_text(chr(value))
##
##                finally:
##                    self.index += 2
##                return

            # ANSI Code Page specification.  If non-English encoding is an issue, this may be where we can determine
            # what encoding we need to use.
            if cw == "ansicpg":
                # Right now, all we do is print a message for programmers who want it if we're dealing with
                # something other than the English Code Page
                if (num != 1252) and DEBUG:
                    print "ansicpg is NOT 1252, US English."

            # Bold
            elif cw == "b":
                # Determine the proper setting in Boolean
                if num:
                    val = (num != 0)
                else:
                    # If no parameter passed, assume to turn it on
                    val = True
                # Set the current font
                self.SetTxtStyle(fontBold = val)

            # Color Blue specification
            elif cw == "blue":
                # Add the blue value to the appropriate color table entry
                self.colorTable[self.colorIndex] |= num

##            # Again, we have a block of code I might still need for Transana, so don't want to remove just yet.  Please ignore it.
##            # Sometimes, the closed dot is encodes as a "bullet" in RTF.
##            elif cw.lower() == 'bullet':
##                # We're using Unicode Character 183
##                tempChar = unichr(183)
##                # And we need to process it at Text
##                self.process_text(tempChar.encode(TransanaGlobal.encoding))

            # Color Table specification
            elif cw == "colortbl":
                # Initialize the Color Table
                self.colorTable = [0x00000]
                # Signal that we are building the Color Table
                self.in_color_table = True

            # Text Background Color or Highlight Color
            elif cw in ["cb", 'highlight']:
                # Get the Color definition from the Color Table
                colorDef = "%06x" % self.colorTable[num]
                # Set the Font Color based on the Color Definition by converting from Hex to Integers
                self.SetTxtStyle(fontBgColor = wx.Color(int(colorDef[:2], 16), int(colorDef[2:4], 16), int(colorDef[4:6], 16)))

            # Foreground (text) color
            elif cw == "cf":
                # Get the Color definition from the Color Table
                colorDef = "%06x" % self.colorTable[num]
                # Set the Font Color based on the Color Definition by converting from Hex to Integers
                self.SetTxtStyle(fontColor = wx.Color(int(colorDef[:2], 16), int(colorDef[2:4], 16), int(colorDef[4:6], 16)))

            # Default font
            elif cw == "deff":
                # Problem:  The Font Table hasn't been defined when this spec arises.
                # Solution:  Remember the default font number and assign it once the Font Table is comp
                self.defaultFontNumber = num

            # Encapsulated Metafile and Windows Metafile format for image processing (not handled)
            elif cw in ['emfblip', 'wmetafile']:
                # Note that we have a Windows Metafile format image that we will not be handling
                self.image_type = 'WMETAFILE'

            # Font number specification
            elif cw == "f":
                # If the font number is NOT already in the Font Table dictionary ...
                if not self.fontTable.has_key(num):
                    # ... we need to add it.  (This should only occur when the Font Table is being read.)
                    # But we don't have all the data we need yet, such as the font name.  So let's just remember
                    # the font number that we just found out for now.
                    self.fontNumber = num
                # If the font number IS in the Font Table ...
                else:
                    # ... set the current Font Face to the appropriate font
                    self.SetTxtStyle(fontFace = self.fontTable[num])

            # First line paragraph indent
            elif cw == 'fi':
                # Update the paragraph first line indent
                self.paragraph['firstlineindent'] = num

            # Field specifier used in URL processing.  Used in many other unsupported ways in RTF as well.
            elif cw == 'field':
                # Indicate that we are in a field
                self.in_field = self.nest

            # Field Instructions, used in URL processing to indicate the URL value
            elif cw == 'fldinst':
                # Signal that we are about to receive a URL
                self.in_url = True

            # Field Result, used in URL processing to indicate the Link Text
            elif cw == 'fldrslt':
                # Signal that we are about to receive the Link Text
                self.in_link = True

            # Font Table declaration
            elif cw == "fonttbl":
                # Signal that we've entered the Font Table
                self.in_font_table = True

            # Font Size
            elif cw == "fs":
                # Set current font size to half the parameter
                self.SetTxtStyle(fontSize = (num / 2))

            # Color Green specification
            elif cw == "green":
                # Add the color to the appropriate color table entry
                self.colorTable[self.colorIndex] |= (num << 8)

            # Italics
            elif cw == "i":
                # Determine the proper setting
                if num:
                    val = (num != 0)
                else:
                    # If no parameter passed, assume to turn it on
                    val = True
                # Set the current font
                self.SetTxtStyle(fontItalic = val)

            # Info block
            elif cw == "info":
                # This block contains metadata such as author/title, ignore it by skipping to the end of the RTF block
                self.seek_eob()

            # JPEG image (untested)
            elif cw == 'jpegblip':
                # Signal that we're dealing with a JPEG image
                self.image_type = wx.BITMAP_TYPE_JPEG
                # Are we in a nested/hidden picture situation?  If so, CAPTURE THE DATA!!!!
                # (This shouldn't be necessary, but can't hurt.)
                if not self.in_image:
                    self.in_image = True

            # Left and right double quote
            elif cw == "ldblquote" or cw == "rdblquote":
                # Add the straight double-quote character
                self.process_text('"')

            # Left paragraph indent
            elif cw == 'li':
                # Update the paragraph left indent
                self.paragraph['leftindent'] = num

            # New Line specifier
            elif cw == 'line':
                # Insert a Newline, but don't change any settings
                self.txtCtrl.Newline()

            # List Text specified (bulleted lists with characters as the bullet text)
            elif cw == 'listtext':
                # Remember that we are in a list
                self.in_list = True
                # Initialize the List Text (probably redundantly)
                self.list_txt = ''

            # Left single quote
            elif cw == "lquote":
                # Add the correct character
                self.process_text("`")

            # Mac Picture (DrawGraph?) format? for image processing (not handled)
            elif cw == 'macpict':
                # Note that we are in an image (Necessary for Word for the Mac support?)
                self.in_image = True
                # Note that we have a Windows Metafile format image that we will not be handling
                self.image_type = 'MACPICT'

            # Paragraph End specifier
            elif cw in ["par"]:
                # The wxRichTextCtrl sets paragraph formatting by specifying it before a Newline() and cancelling it after.
                # It doesn't matter if the paragraph text is already in place.

                # Set the wxRichTextCtrl's tab information
                if len(self.paragraph['tabs']) > 0:
                    self.SetTxtStyle(parTabs = self.paragraph['tabs'])

                # Set the wxRichTextCtrl's paragraph spacing
                self.SetTxtStyle(parSpacingBefore = self.antitwips(self.paragraph['spacingbefore']), parSpacingAfter = self.antitwips(self.paragraph['spacingafter']))
                # Set the wxRichTextCtrl's paragraph alignment
                if self.paragraph['alignment'] == 'center':
                    self.SetTxtStyle(parAlign = wx.TEXT_ALIGNMENT_CENTER)
                elif self.paragraph['alignment'] == 'right':
                    self.SetTxtStyle(parAlign = wx.TEXT_ALIGNMENT_RIGHT)
                # Set the wxRichTextCtrl's line spacing
                self.SetTxtStyle(parLineSpacing = self.paragraph['linespacing'])
                # Set the wxRichTextCtrl's paragraph left, first line, and right indents
                self.SetTxtStyle(parLeftIndent = (self.antitwips(self.paragraph['leftindent'] + self.paragraph['firstlineindent']), self.antitwips(0 - self.paragraph['firstlineindent'])),
                                 parRightIndent = self.antitwips(self.paragraph['rightindent']))
                # Specify the Newline() placement
                self.txtCtrl.Newline()

            # Paragraph Definition
            elif cw == 'pard':
                # If we are NOT in a list ...  (Lists need to preserve formatting!)
                if not self.in_list:
                    # ... reset all paragraph formatting.
                    self.paragraph = {'alignment'       : 'left',
                                      'linespacing'     : richtext.TEXT_ATTR_LINE_SPACING_NORMAL,
                                      'leftindent'      : 0,
                                      'rightindent'     : 0,
                                      'firstlineindent' : 0,
                                      'spacingbefore'   : 0,
                                      'spacingafter'    : 0,
                                      'tabs'            : []}
                    # (We need to reset the paragraph formatting in self.txtAttr as well.)
                    self.SetTxtStyle(parAlign = wx.TEXT_ALIGNMENT_LEFT, parLineSpacing = richtext.TEXT_ATTR_LINE_SPACING_NORMAL,
                                     parTabs = [], parLeftIndent = (0, 0), parRightIndent = 0, parSpacingBefore = 0, parSpacingAfter = 0)

            # Picture (image) processing
            elif cw == 'pict':
                # Signal that we are processing an image
                self.in_image = True

            # Plain Font formatting
            elif cw == "plain":
                self.SetTxtStyle(fontUnderline = False, fontBold = False, fontItalic = False)

            # PNG graphic format image processing
            elif cw == 'pngblip':
                # Signal that our image type is PNG
                self.image_type = wx.BITMAP_TYPE_PNG
                # Are we in a nested/hidden picture situation?  If so, CAPTURE THE DATA!!!!
                # (This shouldn't be necessary, but can't hurt!)
                if not self.in_image:
                    self.in_image = True

            # Center paragraph alignment
            elif cw == 'qc':
                # Update the paragraph alignment
                self.paragraph['alignment'] = 'center'

            # Left paragraph alignment
            elif cw == 'ql':
                # Update the paragraph alignment
                self.paragraph['alignment'] = 'left'

            # Right paragraph alignment
            elif cw == 'qr':
                # Update the paragraph alignment
                self.paragraph['alignment'] = 'right'

            # Color Red specification
            elif cw == "red":
                # Check to see if entry needs to be added
                if self.colorIndex == len(self.colorTable):
                    # If so, add the new entry
                    self.colorTable.append(num << 16)
                # If not,
                else:
                    # update the appropriate entry
                    self.colorTable[self.colorIndex] = num << 16

            # Right paragraph indent
            elif cw == 'ri':
                # Update the paragraph right indent
                self.paragraph['rightindent'] = num

            # Right single quote
            elif cw == "rquote":
                # Add the correct character
                self.process_text("'")

            # rtf version specifier
            elif cw == "rtf":
                # Report if desired
                if DEBUG:
                    print "Document uses RTF version %d" % num
                # There's nothing to do.
                pass

            # Paragraph line spacing after
            elif cw == 'sa':
                # Update the paragraph line spacing after
                self.paragraph['spacingafter'] = num

            # Paragraph line spacing before
            elif cw == 'sb':
                # Update the paragraph line spacing before
                self.paragraph['spacingbefore'] = num

            # Line Spacing
            elif cw == 'sl':
                # NOTE:  The wxRichTextCtrl has limited line spacing options.
                # Double Spacing is 3 lines per inch, or 480 twips
                if num >= 480:
                    # Update the paragraph linespacing
                    self.paragraph['linespacing'] = richtext.TEXT_ATTR_LINE_SPACING_TWICE
                # Line and a half spacing is 4 lines per inch, or 360 twips
                elif num >= 360:
                    # Update the paragraph linespacing
                    self.paragraph['linespacing'] = richtext.TEXT_ATTR_LINE_SPACING_HALF
                # Single spacing is 6 lines per inch, or 240 twips, but that is the default for RTF.
                else:
                    # Update the paragraph linespacing
                    self.paragraph['linespacing'] = richtext.TEXT_ATTR_LINE_SPACING_NORMAL

            # Shape Name and Shape Value
            elif cw in ["sn", "sv"]:
                # We can skip this data while processing images by skipping to the end of the RTF block
                self.seek_eob()

            # Style sheets, and styles in general, are not currently supported.
            elif cw == "stylesheet":
                # Ignore stylesheet data as it messes things up if not properly supported by skipping to the end of the RTF block
                self.seek_eob()

            # Tab
            elif cw == "tab":
                # If we're in a list ...
                if self.in_list:
                    # ... add the tab to the list text.  (We're not ready to add it to the control yet.)
                    self.list_txt += '\t'
                # If we're not in a list ...
                else:
                    # ... send the Tab character to the text processor
                    self.process_text("\t")

            # Tab Stop specification
            elif cw == 'tx':
                # Append the tab stop data to the paragraph's tab stop definition
                self.paragraph['tabs'].append(self.antitwips(num))

            # Unicode Character Processing
            elif cw == 'u':

                if DEBUG and (num not in [164, 8232]):
                    print "Processing Unicode Character Code %d" % num

                # Start exception handling
                try:
                    # Unicode character 8232 is a line separator!
                    if num == 8232:
                        self.txtCtrl.Newline()
                    # Otherwise ...
                    else:
                        # ... convert the number to a unicode character ...
                        tempChar = unichr(num)
                        # ... and process the character as text
                        self.process_text(tempChar)

                        # Sometimes, especially in RTF from Word on the Mac, there are redundant specifiers of the RTF character.
                        # This code detects that and skips over it!
                        if (self.buffer[self.index : self.index + 2] == "\\'") and \
                           (self.buffer[self.index + 2] in '0123456789ABCDEFabcdef') and \
                           (self.buffer[self.index + 3] in '0123456789ABCDEFabcdef') and \
                           (self.buffer[self.index + 4] != '\\'):
                            # Skip past the unicode character digits
                            self.index += 4
                        # If we don't have this condition, se can just look for the next space and set the index after that
                        else:
                            self.index = self.buffer.find(' ', self.index) + 1
                # If a ValueError is raised ...
                except ValueError:
                    # Report to the programmer if desired
                    if DEBUG:
                        print "ValueError in RTF Processing for Unicode.  Control Word 'u', num =", num
                    # ... and just move on.
                    pass

            elif cw == "ul":
                # Determine the proper setting
                if num:
                    val = (num != 0)
                else:
                    # If no parameter passed, assume to turn it on
                    val = True
                # Set the current font
                self.SetTxtStyle(fontUnderline = val)







            # Control Words I have chosen to IGNORE for now  (in groups, but kind of alphabetical beyond that!)

            # ab, ai                      Associated Font characteristics (bold, italic)
            # adeflang, adeff             Default southeast asian language, font
            # aendnotes, aenddoc          End Notes
            # af, afs                     associated font & font size
            # alang                       associated language
            # ansi, mac, pc               Default Character Sets (I don't know what to DO about this!)
            # bliptag
            # charrsid
            # cgrid                       character grid (??)
            # deflang, deflangfe          Default language definition, Default East Asian language
            # dghspace, dgvspace, dghorigin, dgvorigin  Grid drawing information
            # dghshow, dgvshow            Grid drawing information
            # dntblnsbdb                  Something about balancing Japanese characters
            # donotembedlingdata
            # donotembedsysfont
            # expshrtn                    Expand characters spaces on line-ending
            # faauto                      Font Alignment - Auto
            # fbidi, fmodern, fnil, froman, fscript, fswiss  Font family specifications.  At this time, I'm only dealing with specific fonts, not families.
            # fcharset                    Character Set spec.
            # fcs                         something about complex script
            # fet                         Footnote type
            # flomajor, fdbmajor, fhimajor, fbimajor, flominor, fdbminor, fhiminor, fbiminor     ... ummmmm.
            # fprq                        Specifies whether a font uses the default pitch (0), a fixed pitch (1), or a variable pitch (2)  (I don' know the implications for this setting.)
            # ftntj, ftntbj               Footnote justification
            # grfdocevents
            # gutter                      Gutter Width in twips
            # horzdoc, vertdoc            Horizontal or vertical rendering
            # ignoremixedcontent
            # ilfomacatclnup
            # insrsid
            # itap                        paragraph nesting level
            # jclisttab
            # jcompress                   Justification compression
            # kerning                     Point size for kerning (0 is off)
            # lang, langfe                Language settings
            # langnp, langfenp            Language for a text run
            # lin, rin                    left, right paragraph indent
            # linex                       Distance from line number to left margin
            # loch, hich, dbch            Text is single-byte low ansi, hi ansi, double-byte
            # ls                          List Override index
            # margl, margr, margt, margb  Page Margins in "twips".  Not a concept Transana has.  Exports at 1440, 1 inch
            # mmathPr, mmathFont, mbrkBin, mbrkBinSub,
            # msmallFrac, mdispDef, mlMargin, mrMargin,
            # mwrapRight, mintLim, mnaryLim
            # nolnhtadjtbl                No line height adjustment in table
            # nonshppict                  "Specifies a picture destination that it will not read on input" whatever that means.
            # noqfpromote
            # nospaceforul                No space for underlining
            # noultrlspc                  Don't underline trailing spaces
            # noxlattoyen                 Yen Backslash option
            # paperw, paperh              Paper Size in "twips".  Not a concept Transana has.  Exports at 12240 x 15840, 8.5 x 11 inches
            # pararsid
            # picprop, picscalex, picscaley, piccropl, piccropr, piccropt, piccropb,
            # picw, pich, picwgoal, pichgoal
            # relyonvml
            # rsidroot                    Start of Document History (first save)
            # rtlch, ltrch, ltrpar, lrtsect    right-to-left and left-to-right segment directionality
            # saveinvalidxml
            # sectd, sectdefaultcl        default section properties
            # sftntj, sftnbj              Footnote Justification
            # showplaceholdtext
            # showxmlerrors
            # shppict, shplid
            # slmult                      Line Spacing is a multiple of normal
            # sp
            # stshfloch                   Default ASCII font for style sheets.  At this time, I'm not supporting style sheets.
            # stshfhich                   Default High-ANSI font for style sheets
            # stshfdbch                   Default East Asian font for style sheets
            # stshfbi                     Default Complex Script for style sheets
            # themelang, themelangfe, themelangcs  Theme languages
            # trackformatting
            # trackmoves,
            # uc                          Unicode byte length
            # upr                         keyword representation (??)
            # validatexml
            # viewkind                    The "view mode"  (None, page layout, outline view, etc.)
            # viewscale
            # widowctl, widowctrl, widctlpar, nowidctlpar   Widow/orphan control
            # wrapdefault                 use default line wrapping

            elif (cw in ['ab', 'ai',
                        'adeflang', 'adeff',
                        'aendnotes', 'aenddoc',
                        'af', 'afs',
                        'alang',
                        'ansi', 'mac', 'pc',
                        'cgrid',
                        'deflang', 'deflangfe',
                        'dghspace', 'dgvspace', 'dghorigin', 'dgvorigin', 'dghshow', 'dgvshow',
                        'dntblnsbdb',
                        'donotembedlingdata',
                        'donotembedsysfont',
                        'expshrtn',
                        'faauto',
                        'fbidi', 'fmodern', 'fnil', 'froman', 'fscript', 'fswiss',
                        'fcharset',
                        'fcs',
                        'fet',
                        'flomajor', 'fdbmajor', 'fhimajor', 'fbimajor', 'flominor', 'fdbminor', 'fhiminor', 'fbiminor',
                        'fprq',
                        'ftntj', 'ftnbj',
                        'grfdocevents',
                        'gutter',
                        'horzdoc', 'vertdoc',
                        'ignoremixedcontent',
                        'ilfomacatclnup',
                        'insrsid',
                        'itap',
                        'jclisttab',
                        'jcompress',
                        'kerning',
                        'lang', 'langfe', 'langnp', 'langfenp',
                        'lin', 'rin',
                        'linex',
                        'loch', 'hich', 'dbch',
                        'ls',
                        'margl', 'margr', 'margt', 'margb',
                        'mmathPr', 'mmathFont', 'mbrkBin', 'mbrkBinSub', 'msmallFrac', 'mdispDef', 'mlMargin', 'mrMargin', 'mwrapRight',
                        'mintLim', 'mnaryLim',
                        'nolnhtadjtbl',
                        'nonshppict',
                        'noqfpromote',
                        'nospaceforul',
                        'noultrlspc',
                        'noxlattoyen',
                        'paperw', 'paperh',
                        'pararsid',
                        'picprop', 'picscalex', 'picscaley', 'piccropl', 'piccropr', 'piccropt', 'piccropb',
                        'picw', 'pich', 'picwgoal', 'pichgoal',
                        'relyonvml',
                        'rsidroot',
                        'rtlch', 'ltrch', 'ltrpar', 'ltrsect',
                        'saveinvalidxml',
                        'sectd', 'sectdefaultcl',
                        'sftntj', 'sftnbj',
                        'showplaceholdtext',
                        'showxmlerrors',
                        'shppict', 'shplid',
                        'slmult',
                        'sp',
                        'stshfloch', 'stshfhich', 'stshfdbch', 'stshfbi',
                        'themelang', 'themelangfe', 'themelangcs',
                        'trackmoves',
                        'trackformatting',
                        'uc',
                        'upr',
                        'validatexml',
                        'viewkind', 'viewscale',
                        'widowctl', 'widowctrl', 'widctlpar', 'nowidctlpar',
                        'wrapdefault']) or \
                ('bliptag' in cw.lower()) or \
                ('charrsid' in cw.lower())   :
                if DEBUG:
                    print "Ignoring Control Word '%s'" % cw
                else:
                    pass

            else:
                if DEBUG or DEBUG2:
                    numstr = ''
                    if num:
                        numstr = '(' + str(num) + ')'
                    print "Ignoring unknown control word %s%s" % (cw, numstr)

        # Handle the IndexError exception
        except IndexError:
            if DEBUG:
                # Display the Exception Message, allow "continue" flag to remain true
                print "Caught IndexError exception (aborting control word)"
                import sys, traceback
                print "Exception %s: %s" % (sys.exc_info()[0], sys.exc_info()[1])
                traceback.print_exc(file=sys.stdout)
            return

    def process_end_block(self):
        """ Special Processing for the end of an RTF block """
        # Increment the pointer to the current position in the RTF string
        self.index += 1

        # If we're in the Font Table ...
        if self.in_font_table:
            # ... then this signals that we're leaving the font table.
            self.in_font_table = False
            # Set the current text attribute to the default font face
            self.SetTxtStyle(fontFace = self.fontTable[self.defaultFontNumber])
            # Setting the Basic Style sets the wxRichTextCtrl's default font
            self.txtCtrl.SetBasicStyle(self.txtAttr)

        # If we're in the Color Table ...
        if self.in_color_table:
            # ... then this signals that we're leaving the color table
            self.in_color_table = False

        # If we're in an image specification ...
        if self.in_image:
            # ... then this signals that the image specification is over ...
            self.in_image = False
            # ... and we should also reset the image type.
            self.image_type = None

        # If we're in a field (Hyperlink) specification ...
        if self.in_field > 0:
            # ... if we're waiting for the URL ...
            if self.in_url:
                # ... we can stop waiting ...
                self.in_url = False
            # ... if we're waiting for the Link text ...
            if self.in_link:
                # ... we can stop waiting ...
                self.in_link = False
            # ... and the field specification is now over.
            self.in_field = 0

        # If we're in a list specification ...
        if self.in_list:
            # ... then the list specification is probably over now.
            self.in_list = False

    def seek_eob(self):
        """ Seek to the end of the current RTF block. """
        # Note our current nesting level, knowing that we're currently IN the block we want to leave
        desired_nest = self.nest - 1
        # note our current position in the RTF text
        x = self.index
        # As long as we don't reach the end of the RTF text ...
        while x < len(self.buffer):
            # ... look for backslashes and skip them
            if self.buffer[x] == "\\":
                x = x + 1
            # Look for new block starts ...
            elif self.buffer[x] == "{":
                # ... which increase our level of nesting
                self.nest = self.nest + 1
            # Look for block ends ...
            elif self.buffer[x] == "}":
                # ... which decrease out level of nesting
                self.nest = self.nest - 1
                # When we've reached the closer of our current RTF block ...
                if self.nest == desired_nest:
                    # ... we can stop iterating
                    break
            # Move to the next position in the RTF text
            x = x + 1
        # We can now set the new position in the RTF text for processing after the end of the RTF block
        self.index = x + 1

    def antitwips(self, num):
        """ Convert from twips to 10ths of a millimeter, which is what the wxRichTextCtrl uses """
        return int((num * 254 / 72) /20)

# If we're running in stand-alone test mode
if __name__ == '__main__':
    # Create an xml.sax parser
    parser = xml.sax.make_parser()
    # Define our XML to RTF Handler
    handler = XMLToRTFHandler()
    # Set the parser to use the handler
    parser.setContentHandler(handler)
    # Open a test XML file, 'test.xml', which should be created by saving XML from a wxRichTextCtrl, and parse it
    parser.parse("test.xml")
    # Save the resulting RTF string to a file called 'text.rtf'
    handler.saveFile("test.rtf")

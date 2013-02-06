#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##This file is part of pySequence
#############################################################################
#############################################################################
##                                                                         ##
##                                   Options                               ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2012 C�drick FAURY

#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


import ConfigParser
import os.path
import recup_excel
import io

import wx.combo
#from constantes import *
import constantes


##############################################################################
#      Options     #
##############################################################################
class Options:
    """ D�finit les options de pySequence """
    def __init__(self, options = None):
        #
        # Toutes les options ...
        # Avec leurs valeurs par d�faut.
        #
        self.optClasse = {}
        self.optSystemes = {}
#        self.optGenerales = {}
#        self.optImpression = {}
#        self.optCalcul = {}
#        
        if options == None:
            self.defaut()
          
#        self.listeOptions = [u"G�n�ral", u"Affichage", u"Couleurs", u"Impression"] 
         
        self.typesOptions = {u"Classe" : self.optClasse,
                             u"Syst�mes" : self.optSystemes,
#                             u"Calcul" : self.optCalcul,
#                             u"Couleurs" : self.optCouleurs,
#                             u"Impression" : self.optImpression,
                             }
        
        
        # Le fichier o� seront sauv�es les options
        self.fichierOpt = os.path.join(constantes.APP_DATA_PATH, "sequence.cfg")
        
        

    #########################################################################################################
    def __repr__(self):
        print self.optClasse
        return ""
    
#        t = "Options :\n"
#        for o in self.optClasse.items():
#            if type(o[1]) == int or type(o[1]) == float:
#                tt = str(o[1])
#            elif type(o[1]) == bool:
#                tt = str(o[1])
#            else:
#                tt = ""
#                ttt = o[1]
#                print ttt, type(ttt)
#            t += "\t" + o[0] + " = " + tt +"\n"
#        return t
    
    
    #########################################################################################################
    def fichierExiste(self):
        """ V�rifie si le fichier 'options' existe
        """
#        PATH=os.path.dirname(os.path.abspath(sys.argv[0]))
#        os.chdir(globdef.PATH)
        if os.path.isfile(self.fichierOpt):
            return True
        return False

    #########################################################################################################
    def enregistrer(self):
        """" Enregistre les options dans un fichier
        """
#        print "Enregistrement",self
        config = ConfigParser.ConfigParser()

        for titre,dicopt in self.typesOptions.items():
            titre = titre.encode('utf-8')
            config.add_section(titre)
            for opt in dicopt.items():
                
                if type(opt[1]) == list:
                    for i,v in enumerate(opt[1]):
                        config.set(titre, opt[0]+"_"+str(i), "-"+v+"-")
                
                elif type(opt[1]) == dict:
                    for k,v in opt[1].items():
                        config.set(titre, opt[0]+"_"+k, v)
                
                else:
                    config.set(titre, opt[0], opt[1])
        
        config.write(open(self.fichierOpt,'w'))



    ############################################################################
    def ouvrir(self, encoding = 'utf_8_sig'):
        """ Ouvre un fichier d'options 
        """
        config = ConfigParser.ConfigParser()
        try :
            with io.open(self.fichierOpt, 'r', encoding=encoding) as fp:
                config.readfp(fp)
        except:
            with io.open(self.fichierOpt, 'r', encoding='utf_8_sig') as fp:
                config.readfp(fp)
        config.read(self.fichierOpt)
        print "ouverture :",self.fichierOpt
        for titre in self.typesOptions.keys():
            titreUtf = titre.encode('utf-8')
#            print titreUtf, self.typesOptions[titre].keys()
            for titreopt in self.typesOptions[titre].keys():
                opt = self.typesOptions[titre][titreopt] 
#                print type(opt), opt
                if type(opt) == int:
                    opt = config.getint(titreUtf, titreopt)
                elif type(opt) == float:
                    opt = config.getfloat(titreUtf, titreopt)
                elif type(opt) == bool:
                    opt = config.getboolean(titreUtf, titreopt)
                elif type(opt) == str or type(opt) == unicode:
                    opt = config.get(titreUtf, titreopt)
                elif isinstance(opt, wx._gdi.Colour):
                    v = eval(config.get(titreUtf, titreopt))
                    opt = wx.Colour(v[0], v[1], v[2], v[3])
                elif type(opt) == list:
                    d = {}
                    for n, v in config.items(titreUtf):
#                        print titreopt, n
                        if titreopt.lower() in n:
                            d[eval(n.rsplit("_")[-1])] = unicode(config.get(titreUtf, n))
#                    print d, "-->",
                    
                    l = []
                    for i in range(len(d)):
                        l.append(d[i][1:-1])
                    opt = l
#                    print l, type(l[0])
                    
                elif type(opt) == dict:
                    d = {}
                    for n, v in config.items(titreUtf):
                        if titreopt.lower() in n:
                            d[n.rsplit("_")[-1].upper()] = eval(config.get(titreUtf, n))
                    opt = d
                    
                # pour un passage correct de la version 2.5 � 2.6
                try:
                    v = eval(opt)
                    if type(v) == tuple:
                        opt = wx.Colour(v[0], v[1], v[2]).GetAsString(wx.C2S_HTML_SYNTAX)
#                    print "  ", opt
                except:
                    pass
                
                self.typesOptions[titre][titreopt] = opt
                
                
        


    ############################################################################
    def copie(self):
        """ Retourne une copie des options """
        options = Options()
        for titre,dicopt in self.typesOptions.items():
            titre.encode('utf-8')
            nopt = {}
            for opt in dicopt.items():
                options.typesOptions[titre][opt[0]] = opt[1]
#                nopt[opt[0]] = opt[1]
#            options.typesOptions[titre] = (options.typesOptions[titre][0], nopt)
      
        return options
                
#        self.proposerAnimMont.set(options.proposerAnimMont.get())
#        self.proposerAnimArret.set(options.proposerAnimArret.get())
#        self.proposerChaines.set(options.proposerChaines.get())
#        self.typeAide.set(options.typeAide.get())
#        self.repertoireCourant.set(options.repertoireCourant.get())

        
    ############################################################################
    def defaut(self):
        print "Options defaut"
        self.definir()
        
    ############################################################################
    def definir(self):
#        self.optClasse["TypeEnseignement"] = TYPE_ENSEIGNEMENT
        self.optClasse["Effectifs"] = {"C" : constantes.Effectifs["C"],
                                       "G" : constantes.NbrGroupes["G"],
                                       "E" : constantes.NbrGroupes["E"],
                                       "P" : constantes.NbrGroupes["P"]}
        self.optClasse["CentresInteretET"] = [ci for ci in constantes.CentresInterets_ET]
        self.optClasse["PositionsCI_ET"] = [po for po in constantes.PositionCibleCI_ET]
        self.optClasse["TypeEnseignement"] = "SSI"
        
        self.optSystemes["Systemes"] = []
        self.optSystemes["Nombre"] = []
        

    ############################################################################
    def valider(self, classe):
        self.optClasse["Effectifs"] = {"C" : classe.effectifs["C"],
                                       "G" : classe.nbrGroupes["G"],
                                       "E" : classe.nbrGroupes["E"],
                                       "P" : classe.nbrGroupes["P"]}
        if hasattr(classe, 'ci_ET'):
            self.optClasse["CentresInteretET"] = classe.ci_ET
            self.optClasse["PositionsCI_ET"] = classe.posCI_ET
        
        self.optClasse["TypeEnseignement"] = classe.typeEnseignement
        
    ############################################################################
    def validerSystemes(self, sequence):
        for syst, nbr in sequence.GetNbrSystemes().items():
            if syst in self.optSystemes["Systemes"]:
                i = self.optSystemes["Systemes"].index(syst)
                self.optSystemes["Nombre"][i] = str(max(self.optSystemes["Nombre"][i], nbr))
            else:
                self.optSystemes["Systemes"].append(syst)
                self.optSystemes["Nombre"].append(str(nbr))
  
        
    ###########################################################################
    def extraireRepertoire(self,chemin):
        for i in range(len(chemin)):
            if chemin[i] == "/":
                p = i
        self.repertoireCourant = chemin[:p+1]
        return chemin[:p+1]
        
        
##############################################################################
#     Fen�tre Options     #
##############################################################################
class FenOptions(wx.Dialog):
#   "Fen�tre des options"      
    def __init__(self, parent, options):
        wx.Dialog.__init__(self, parent, -1, u"Options de pySequence")#, style = wx.RESIZE_BORDER)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.options = options
        self.parent = parent
        
        
        #
        # Le book ...
        #
        nb = wx.Notebook(self, -1)
        nb.AddPage(pnlClasse(nb, options.optClasse), u"Classe")
#        nb.AddPage(pnlAffichage(nb, options.optAffichage), _(u"Affichage"))
#        nb.AddPage(pnlCalcul(nb, options.optCalcul), _(u"Calcul"))
#        nb.AddPage(pnlImpression(nb, options.optImpression), _(u"Impression"))
#        nb.AddPage(pnlCouleurs(nb, options.optCouleurs), _(u"Couleurs"))
        nb.SetMinSize((400,-1))
        sizer.Add(nb, flag = wx.EXPAND)#|wx.ALL)
        self.nb = nb
        
        #
        # Les boutons ...
        #
        btnsizer = wx.StdDialogButtonSizer()
        
        if wx.Platform != "__WXMSW__":
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)
        
        btn = wx.Button(self, wx.ID_OK)
        help = u"Valider les changements apport�s aux options"
        btn.SetToolTip(wx.ToolTip(help))
        btn.SetHelpText(help)
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        help = u"Annuler les changements et garder les options comme auparavant"
        btn.SetToolTip(wx.ToolTip(help))
        btn.SetHelpText(help)
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        
        btn = wx.Button(self, -1, u"D�faut")
        help = u"R�tablir les options par d�faut"
        btn.SetToolTip(wx.ToolTip(help))
        btn.SetHelpText(help)
        self.Bind(wx.EVT_BUTTON, self.OnClick, btn)
        bsizer = wx.BoxSizer(wx.HORIZONTAL)
        bsizer.Add(btn)
        bsizer.Add(btnsizer, flag = wx.EXPAND|wx.ALIGN_RIGHT)
        
        sizer.Add(bsizer, flag = wx.EXPAND)#|wx.ALL)
        self.SetMinSize((400,-1))
#        print self.GetMinSize()
#        self.SetSize(self.GetMinSize())
        self.SetSizerAndFit(sizer)
        
    def OnClick(self, event):
        self.options.defaut()
        
        for np in range(self.nb.GetPageCount()):
            
            p = self.nb.GetPage(np)
#            print "   ",p
            for c in p.GetChildren():
#                print c
                c.Destroy()
#            p.DestroyChildren()
#            print p.GetSizer().GetChildren()
            p.CreatePanel()
            p.Layout()
        
        
        
#############################################################################################################
class pnlClasse(wx.Panel):
    def __init__(self, parent, optGene):
        
        wx.Panel.__init__(self, parent, -1)
        
        self.opt = optGene
        
        self.CreatePanel()
    
        
    
    def CreatePanel(self):
        
        self.ns = wx.BoxSizer(wx.VERTICAL)
        
        #
        # Type d'enseignement
        #
        sb0 = wx.StaticBox(self, -1, u"Type d'enseignement", size = (200,-1))
        sbs0 = wx.StaticBoxSizer(sb0,wx.VERTICAL)
        
        
        cb = wx.ComboBox(self, -1,"", size = (40, -1), 
                         choices = constantes.listEnseigmenent,
                         style = wx.CB_DROPDOWN|wx.CB_READONLY )
        cb.SetStringSelection(self.opt["TypeEnseignement"])
        cb.SetToolTip(wx.ToolTip(u"Choisir le type d'enseignement" ))
        sbs0.Add(cb, flag = wx.EXPAND|wx.ALL, border = 5)
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, cb)
        self.ns.Add(sbs0, flag = wx.EXPAND|wx.ALL)
        
        
        #
        # Centres d'int�r�t
        #
        sb1 = wx.StaticBox(self, -1, u"Centres d'int�r�t ET", size = (200,-1))
        sbs1 = wx.StaticBoxSizer(sb1,wx.VERTICAL)
        txt = wx.TextCtrl(self, -1, self.opt["CentresInteretET"],
                          style = wx.TE_MULTILINE)
        sbs1.Add(txt, flag = wx.EXPAND|wx.ALL, border = 5)
        txt.Bind(wx.EVT_TEXT, self.EvtTxtCI)
        self.txtCi = txt
        if self.opt["TypeEnseignement"] != 'ET' :
            self.txtCi.Enable(False)
        btn = wx.Button(self, -1, u"S�lectionner")
        help = u"S�lectionner depuis un fichier Excel"
        btn.SetToolTip(wx.ToolTip(help))
        btn.SetHelpText(help)
        sbs1.Add(btn, flag = wx.EXPAND|wx.ALL, border = 5)
        self.Bind(wx.EVT_BUTTON, self.SelectCI, btn)
        self.ns.Add(sbs1, flag = wx.EXPAND|wx.ALL)    
        
        #
        # Effectifs
        #
        sb3 = wx.StaticBox(self, -1, u"Effectifs", size = (200,-1))
        sbs3 = wx.StaticBoxSizer(sb3,wx.VERTICAL)
        varEff = []
        for i, eff in enumerate(constantes.listeEffectifs):
            v = Variable(constantes.Effectifs[eff][0],  
                         lstVal = self.opt["Effectifs"].split()[i], 
                         typ = VAR_ENTIER_POS, bornes = [1,40])
            varEff.append(v)
            vc = VariableCtrl(self, v, coef = 1, labelMPL = False, signeEgal = False,
                              help = u"Nombre d'�l�ves")
            self.Bind(EVT_VAR_CTRL, self.EvtVariableEff, vc)
            sbs3.Add(vc, flag = wx.EXPAND|wx.ALL, border = 2)
        self.ns.Add(sbs3, flag = wx.EXPAND|wx.ALL)
        self.varEff = varEff
        self.SetSizerAndFit(self.ns)
    
    
        
    ######################################################################################  
    def EvtComboBox(self, event):
        print event.GetEventObject().GetValue()
        self.opt["TypeEnseignement"] = event.GetEventObject().GetValue()
        if self.opt["TypeEnseignement"] != 'ET' :
            self.txtCi.Enable(False)
        else:
            self.txtCi.Enable(True)
        
    ######################################################################################  
    def EvtTxtCI(self, event):
        self.opt["CentresInteretET"] =  event.GetString()
        
        
    ######################################################################################  
    def EvtVariableEff(self, event):
        i = self.varEff.index(event.GetVar())
        te = self.opt["Effectifs"].split()
        te[i] = str(event.GetVar().v[0])
        t = " "
        self.opt["Effectifs"] = t.join(te)


    ######################################################################################  
    def SelectCI(self, event = None):
        if recup_excel.ouvrirFichierExcel():
            dlg = wx.MessageDialog(self.Parent, u"S�lectionner une liste de CI\n" \
                                             u"dans le classeur Excel qui vient de s'ouvrir,\n" \
                                             u"puis appuyer sur Ok.\n\n" \
                                             u"Format attendu de la selection :\n" \
                                             u"Liste des CI sur une colonne.",
                                             u'S�lection de CI',
                                             wx.ICON_INFORMATION | wx.YES_NO | wx.CANCEL
                                             )
            res = dlg.ShowModal()
            dlg.Destroy() 
            if res == wx.ID_YES:
                ls = recup_excel.getColonne(c = 0)
                ci = getTextCI(ls)
                self.txtCi.ChangeValue(ci)
                self.opt["CentresInteretET"] = ci
            elif res == wx.ID_NO:
                print "Rien" 

##########################################################################################################
#
#  DirSelectorCombo
#
##########################################################################################################
class DirSelectorCombo(wx.combo.ComboCtrl):
    def __init__(self, *args, **kw):
        wx.combo.ComboCtrl.__init__(self, *args, **kw)

        # make a custom bitmap showing "..."
        bw, bh = 14, 16
        bmp = wx.EmptyBitmap(bw,bh)
        dc = wx.MemoryDC(bmp)

        # clear to a specific background colour
        bgcolor = wx.Colour(255,254,255)
        dc.SetBackground(wx.Brush(bgcolor))
        dc.Clear()

        # draw the label onto the bitmap
        label = "..."
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        dc.SetFont(font)
        tw,th = dc.GetTextExtent(label)
        dc.DrawText(label, (bw-tw)/2, (bw-tw)/2)
        del dc

        # now apply a mask using the bgcolor
        bmp.SetMaskColour(bgcolor)

        # and tell the ComboCtrl to use it
        self.SetButtonBitmaps(bmp, True)
        

    # Overridden from ComboCtrl, called when the combo button is clicked
    def OnButtonClick(self):
        # In this case we include a "New directory" button. 
#        dlg = wx.FileDialog(self, "Choisir un fichier mod�le", path, name,
#                            "Rich Text Format (*.rtf)|*.rtf", wx.FD_OPEN)
        dlg = wx.DirDialog(self, _("Choisir un dossier"),
                           defaultPath = globdef.DOSSIER_EXEMPLES,
                           style = wx.DD_DEFAULT_STYLE
                           #| wx.DD_DIR_MUST_EXIST
                           #| wx.DD_CHANGE_DIR
                           )

        # If the user selects OK, then we process the dialog's data.
        # This is done by getting the path data from the dialog - BEFORE
        # we destroy it. 
        if dlg.ShowModal() == wx.ID_OK:
            self.SetValue(dlg.GetPath())

        # Only destroy a dialog after you're done with it.
        dlg.Destroy()
        
        self.SetFocus()

    # Overridden from ComboCtrl to avoid assert since there is no ComboPopup
    def DoSetPopupControl(self, popup):
        pass



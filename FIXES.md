# Affichage Fiche validation Projet
## Erreur
```
  File "{Python}\lib\site-packages\wx\core.py", line 3285, in <lambda>
    lambda event: event.callable(*event.args, **event.kw) )
  File "{Python}\lib\site-packages\wx\lib\pdfviewer\viewer.py", line 434, in Render
    self.pdfdoc.RenderPage(gc, pageno, scale=self.scale)
  File "{Python}\lib\site-packages\wx\lib\pdfviewer\viewer.py", line 519, in RenderPage
    bmp = wx.Bitmap.FromBufferRGBA(pix.width, pix.height, pix.samples)

Type :  <class 'ValueError'> 
ValueError :  Invalid data buffer size
```

## Fix
https://github.com/wxWidgets/Phoenix/issues/1350

Fichier `{Python}\Lib\site-packages\wx\pdfviewer\viewer.py`, ligne 519 :
```
    def RenderPage(self, gc, pageno, scale=1.0):
        " Render the set of pagedrawings into gc for specified page "
        page = self.pdfdoc.loadPage(pageno)
        matrix = fitz.Matrix(scale, scale)
        try:
            pix = page.getPixmap(matrix=matrix)   # MUST be keyword arg(s)
            #bmp = wx.Bitmap.FromBufferRGBA(pix.width, pix.height, pix.samples)
            bmp = wx.Bitmap.FromBuffer(pix.width, pix.height, pix.samples)
            gc.DrawBitmap(bmp, 0, 0, pix.width, pix.height)
            self.zoom_error = False
        except (RuntimeError, MemoryError):
            if not self.zoom_error:     # report once only
                self.zoom_error = True
                dlg = wx.MessageDialog(self.parent, 'Out of memory. Zoom level too high?',
                              'pdf viewer' , wx.OK |wx.ICON_EXCLAMATION)
                dlg.ShowModal()
                dlg.Destroy()
```
Remplacer
`bmp = wx.Bitmap.FromBufferRGBA(pix.width, pix.height, pix.samples)`
par 
`bmp = wx.Bitmap.FromBuffer(pix.width, pix.height, pix.samples)`



# Problème de curseur dans les zones de description
A chaque nouvelle installation de wxPython :

## Fix
Modifier le fichier `{Python}\Lib\site-packages\wx\lib\agw\supertooltip.py` , ligne 499 :
```
...
def OnDestroy(self, event):
        """
        Handles the ``wx.EVT_LEFT_DOWN``, ``wx.EVT_LEFT_DCLICK`` and ``wx.EVT_KILL_FOCUS``
        events for :class:`SuperToolTip`. All these events destroy the :class:`SuperToolTip`,
        unless the user clicked on one hyperlink.

        :param `event`: a :class:`MouseEvent` or a :class:`FocusEvent` event to be processed.
        """
        _event.Skip()_
        if not isinstance(event, wx.MouseEvent):
           ...
```
Rajouter la ligne `event.Skip()`.
Supprimer le fichier `.pyc` correspondant dans le sous-dossier `__pycache__`.



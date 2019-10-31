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

# Problème de curseur dans les zones de description

## Fix
Modifier le fichier `{Python}\Lib\site-packages\wx\lib\agw\supertooltip.py` :
```
...
def OnDestroy(self, event):
        """
        Handles the ``wx.EVT_LEFT_DOWN``, ``wx.EVT_LEFT_DCLICK`` and ``wx.EVT_KILL_FOCUS``
        events for :class:`SuperToolTip`. All these events destroy the :class:`SuperToolTip`,
        unless the user clicked on one hyperlink.

        :param `event`: a :class:`MouseEvent` or a :class:`FocusEvent` event to be processed.
        """
        event.Skip()
        if not isinstance(event, wx.MouseEvent):
           ...
```
Rajouter la ligne `event.Skip()`.

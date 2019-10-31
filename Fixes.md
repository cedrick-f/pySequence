# Affichage Fiche validation Projet
## Erreur
`
  File "{Python}\lib\site-packages\wx\core.py", line 3285, in <lambda>
    lambda event: event.callable(*event.args, **event.kw) )
  File "{Python}\lib\site-packages\wx\lib\pdfviewer\viewer.py", line 434, in Render
    self.pdfdoc.RenderPage(gc, pageno, scale=self.scale)
  File "{Python}\lib\site-packages\wx\lib\pdfviewer\viewer.py", line 519, in RenderPage
    bmp = wx.Bitmap.FromBufferRGBA(pix.width, pix.height, pix.samples)

Type :  <class 'ValueError'> 
ValueError :  Invalid data buffer size
`

## Fix
https://github.com/wxWidgets/Phoenix/issues/1350

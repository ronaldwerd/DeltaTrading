import wx
from finance_objects import Quote
from wx import glcanvas

APP_TITLE = 'Delta Algorithm'


class PygletGLPanel(wx.Panel):

    def processEraseBackgroundEvent(self, event):
        pass  # Do nothing, to avoid flashing on MSWin

    def processSizeEvent(self, event):
        if wx.VERSION >= (2, 9):
            wx.CallAfter(self.doSetViewport)
        else:
            self.doSetViewport()
        event.Skip()

    def processPaintEvent(self, event):
        if not self.FIRST_PAINT:
            self.FIRST_PAINT = True

        self.PrepareGL()
        self.OnDraw()
        event.Skip()

    def __init__(self, parent, id, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        # Forcing a no full repaint to stop flickering
        style = style | wx.NO_FULL_REPAINT_ON_RESIZE
        self.FIRST_PAINT = False
        # call super function
        super(PygletGLPanel, self).__init__(parent, id, pos, size, style)
        # init gl canvas data
        self.GLinitialized = False
        attribList = (glcanvas.WX_GL_RGBA,  # RGBA
                      glcanvas.WX_GL_DOUBLEBUFFER,  # Double Buffered
                      glcanvas.WX_GL_DEPTH_SIZE, 24)  # 24 bit
        # Create the canvas
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.canvas = glcanvas.GLCanvas(self, attribList=attribList)

        if wx.VERSION >= (2, 9):
            self.context = glcanvas.GLContext(self.canvas)

        self.sizer.Add(self.canvas, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Layout()

        # bind events
        self.canvas.Bind(wx.EVT_ERASE_BACKGROUND, self.processEraseBackgroundEvent)
        self.canvas.Bind(wx.EVT_SIZE, self.processSizeEvent)
        self.canvas.Bind(wx.EVT_PAINT, self.processPaintEvent)



class MainFrame(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(MainFrame, self).__init__(*args, **kwargs)
        self.panel = PygletGLPanel(self, -1)
        self.InitUI()

    def OnQuit(self):
        self.Close()

    def onKeyPress(self, event):
        code = event.GetKeyCode()

        if code == 81:
            self.OnQuit()
    pass

    def InitUI(self):
        menubar = wx.MenuBar()
        file_menu = wx.Menu()
        fitem = file_menu.Append(wx.ID_EXIT, 'Quit', APP_TITLE)
        menubar.Append(file_menu, '&File')
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnQuit, fitem)
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyPress)

        self.SetSize((640, 480))
        self.SetTitle(APP_TITLE)
        self.Centre()
        self.Show(True)

    def updateUI(self, q: Quote):
        pass


def run():
    ex = wx.App()
    MainFrame(None)
    ex.MainLoop()


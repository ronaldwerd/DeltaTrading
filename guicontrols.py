import wx
from finance_objects import Quote

APP_TITLE = 'Delta Algorithm'


class MainFrame(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(MainFrame, self).__init__(*args, **kwargs)
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


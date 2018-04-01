import wx
import pyglet
from wx import glcanvas
from pyglet import gl
from finance_objects import Quote

APP_TITLE = 'Delta Algorithm'


class PygletWXContext(gl.Context):

    def __init__(self, config=None, context_share=None):
        self.config = config
        self.context_share = context_share
        self.canvas = None

        if context_share:
            self.object_space = context_share.object_space
        else:
            self.object_space = gl.ObjectSpace()

    def attach(self, canvas=None):
        pass

    def detach(self):
        pass

    def set_current(self):
        gl.current_context = self
        gl.gl_info.set_active_context()
        gl.glu_info.set_active_context()


class PygletGLPanel(wx.Panel):

    colorSwap = 0

    def create_objects(self):
        '''create opengl objects when opengl is initialized'''
        pass

    def update_object_resize(self, width, height):
        '''called when the window receives only if opengl is initialized'''
        pass

    def draw_objects(self):
        '''called in the middle of ondraw after the buffer has been cleared'''
        # print("X draw event triggered")
        # gl.glClearColor(1, 78, 1, 90)

        gl.glClear(gl.GL_COLOR_BUFFER_BIT)  # Clear the color buffer
        gl.glLoadIdentity()  # Reset model-view matrix
        gl.glBegin(gl.GL_QUADS)

        if self.colorSwap == 1:
            gl.glColor3f(1.0, 0.0, 0.0)
            self.colorSwap = 0
        else:
            gl.glColor3f(0.0, 1.0, 0.0)
            self.colorSwap = 1

        gl.glVertex2f(self.width - 10, 10)
        gl.glVertex2f(self.width - 10, self.height - 10)
        gl.glVertex2f(10.0, self.height - 10)
        gl.glVertex2f(10.0, 10.0)
        gl.glEnd()

        # gl.glBegin(gl.GL_QUADS)
        # line_vertex = [40, 20, 100, 120]
        # gl.glVertexPointer(2, gl.GL_FLOAT, 0, line_vertex)
        # gl.glDrawArrays(gl.GL_LINES, 0, 2)
        # gl.glEnd()
        pass

    def processEraseBackgroundEvent(self, event):
        pass  # Do nothing, to avoid flashing on MSWin

    def processSizeEvent(self, event):
        wx.CallAfter(self.doSetViewport)
        event.Skip()

    def processPaintEvent(self, event):
        if not self.FIRST_PAINT:
            self.FIRST_PAINT = True

        self.PrepareGL()
        self.OnDraw()
        event.Skip()

    def doSetViewport(self):
        self.Show()
        self.PrepareGL()
        # Make sure the frame is shown before calling SetCurrent.
        self.canvas.SetCurrent(self.context)
        size = self.GetGLExtents()
        self.winsize = (size.width, size.height)
        self.width, self.height = size.width, size.height
        if self.width < 0:
            self.width = 1
        if self.height < 0:
            self.height = 1
        self.OnReshape(size.width, size.height)
        self.canvas.Refresh(False)


    def PrepareGL(self):
        self.canvas.SetCurrent(self.context)

        # initialize OpenGL only if we need to
        if not self.GLinitialized:
            self.OnInitGL()
            self.GLinitialized = True
            size = self.GetGLExtents()
            self.OnReshape(size.width, size.height)

        self.pygletcontext.set_current()

    def OnInitGL(self):
        self.pygletcontext.set_current()
        # normal gl init
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glClearColor(201, 45, 75, 241)
        self.create_objects()

    def GetGLExtents(self):
        '''Get the extents of the OpenGL canvas.'''
        return self.canvas.GetClientSize()

    def SwapBuffers(self):
        '''Swap the OpenGL buffers.'''
        self.canvas.SwapBuffers()

    def __init__(self, parent, id, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        self.pygletcontext = PygletWXContext()
        # Forcing a no full repaint to stop flickering
        style = style | wx.NO_FULL_REPAINT_ON_RESIZE
        self.FIRST_PAINT = False
        # call super function
        super(PygletGLPanel, self).__init__(parent, id, pos, size, style)
        # init gl canvas data
        self.GLinitialized = False
        attribute_list = (glcanvas.WX_GL_RGBA,  # RGBA
                          glcanvas.WX_GL_DOUBLEBUFFER,  # Double Buffered
                          glcanvas.WX_GL_DEPTH_SIZE, 24)  # 24 bit

        # Create the canvas
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.canvas = glcanvas.GLCanvas(self, attribList=attribute_list)
        self.context = glcanvas.GLContext(self.canvas)

        self.sizer.Add(self.canvas, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Layout()

        # bind events
        self.canvas.Bind(wx.EVT_ERASE_BACKGROUND, self.processEraseBackgroundEvent)
        self.canvas.Bind(wx.EVT_SIZE, self.processSizeEvent)
        self.canvas.Bind(wx.EVT_PAINT, self.processPaintEvent)
        # self.Bind(wx.EVT_KEY_DOWN, self.onKeyPress)
        # pyglet.clock.schedule_interval(self.OnDraw(), 1.0 / 60)


    def OnReshape(self, width, height):
        '''Reshape the OpenGL viewport based on the dimensions of the window.'''
        # CORRECT WIDTH AND HEIGHT
        if width <= 0:
            width = 1
        if height <= 0:
            height = 1
        if self.GLinitialized:
            self.pygletcontext.set_current()
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0, width, 0, height, 1, -1)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        if self.GLinitialized:
            self.update_object_resize(width, height)

    def OnDraw(self, *args, **kwargs):
        "Draw the window."
        # clear the context
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        # draw objects
        self.draw_objects()
        # update screen
        self.SwapBuffers()


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


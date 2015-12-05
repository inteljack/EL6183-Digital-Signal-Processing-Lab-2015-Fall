#! /usr/local/bin/python
from wpy import *
import string

class CScribDoc(CDocument):
    def __init__(self, templ):
        CDocument.__init__(self, templ)
        self.pen = self.thin_pen = CPen(2, (200, 0, 0)).Create()
        self.thick_pen = CPen(5, (0, 200, 0)).Create()
        self.m_strokeList = []
    def NewStroke(self):
        s = CStroke(self.pen)
        self.m_strokeList.append(s)
        self.SetModifiedFlag()
        return s 
    def OnCloseDocument(self):
        CDocument.OnCloseDocument(self)
        self.pen = None
    def DeleteContents(self):
        self.m_strokeList = []
    def Serialize(self, is_storing):
        print "Nothing happens"
    def OnMenuPenThinpen(self, control):
        if string.find(control.wpyText, "Thick") >= 0:
            self.pen = self.thick_pen
        else:
            self.pen = self.thin_pen

class ScribFrameMenu(CMenu):
    def __init__(self):
        CMenu.__init__(self)
        file        = MenuFile(self)
        edit        = MenuEdit(self)
        pen         = CMenuButton(self, "Pen")
        view        = MenuView(self)
        window      = MenuWindow(self)
        help        = MenuHelp(self)

        # file items:
        new         = MenuFileNew(file)
        close       = MenuFileClose(file)
        CMenuLine(file)
        exit        = MenuFileExit(file)

        # edit items

        # pen items:
        thin             = CMenuRadio(pen, "Thin pen", None)
        thin.wpyMessage  = "Toggles the line thickness between thin and thick"
        thick            = CMenuRadio(pen, "Thick pen", thin)
        thick.wpyMessage = thin.wpyMessage
        thick.wpyHandler = thin.wpyHandler

        # view items
        status           = MenuViewStatusbar(view)
        status.wpyCheckValue = 0
        status.EnableMenuItem(0)

        # window items
        new         = MenuWindowNewwindow(window)
        cascade     = MenuWindowCascade(window)
        tileh       = MenuWindowTilehorz(window)
        tilev       = MenuWindowTilevert(window)
        arrange     = MenuWindowArrangeicons(window)

        # help items
        about       = MenuHelpAbout(help)

class ScribMainFrameMenu(CMenu):
    def __init__(self):
        CMenu.__init__(self)
        file        = MenuFile(self)
        view        = MenuView(self)
        help        = MenuHelp(self)

        # file items:
        new         = MenuFileNew(file)
        CMenuLine(file)
        exit        = MenuFileExit(file)

        # view items
        status      = MenuViewStatusbar(view)

        # help items
        about       = MenuHelpAbout(help)

class CStroke:
    def __init__(self, pen):
        self.pen = pen
        self.m_pointArray = []
    def DrawStroke(self, DC):
        DC.SelectObject(self.pen)
        i = self.m_pointArray[0]
        DC.MoveTo(i[0], i[1])
        for i in self.m_pointArray[1:]:
            DC.LineTo(i[0], i[1])
 
class CScribView(CScrollView):
    def OnCreate(self, event):
        self.m_pStrokeCur = None
        self.m_ptPrev = None
    def OnDraw(self, DC):
        for stroke in self.wpyDocument.m_strokeList:
            stroke.DrawStroke(DC) 
    def OnLButtonDown(self, x, y, flags):
        point = (x, y)
        self.m_pStrokeCur = self.wpyDocument.NewStroke()
        self.m_pStrokeCur.m_pointArray.append(point)
        self.SetCapture()
        self.m_ptPrev = point
        DC = self.GetDC()
        DC.SelectObject(self.wpyDocument.pen)
        self.ReleaseDC(DC)
        return 0
    def OnLButtonUp(self, x, y, flags):
        if GetCapture() != self:
            return
        point = (x, y)
        DC = self.GetDC()
        DC.MoveTo(self.m_ptPrev[0], self.m_ptPrev[1])
        DC.LineTo(x, y)
        self.ReleaseDC(DC)
        self.m_pStrokeCur.m_pointArray.append(point)
        ReleaseCapture()
        self.wpyDocument.UpdateAllViews(self, None)
        self.wpyDocument.SetModifiedFlag(0)
        return 0
    def OnMouseMove(self, x, y, flags):
        if GetCapture() != self:
            return
        point = (x, y)
        self.m_pStrokeCur.m_pointArray.append(point)
        DC = self.GetDC()
        DC.MoveTo(self.m_ptPrev[0], self.m_ptPrev[1])
        DC.LineTo(x, y)
        self.ReleaseDC(DC)
        self.m_ptPrev = point
        return 0

class MyApp(CWinApp):
    def InitInstance(self):
        templ = CMultiDocTemplate(CScribDoc,
                                  CMDIChildWnd,
                                  CScribView,
                                  ScribFrameMenu)
        templ.wpyText = "Python Scribble"
        self.AddDocTemplate(templ)
        main_frame = CMDIFrameWnd()
        main_frame.wpyStatusLine = CStatusBar(self, "")
        # Menu when there are no frames
        main_frame.wpyMenu = ScribMainFrameMenu()
        main_frame.Create()
        self.FileNew()

# Start the application, respond to events.
app = MyApp()


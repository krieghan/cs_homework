#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
# generated by wxGlade 0.4.1 on Wed May 24 16:06:35 2006

import wx
import sys
from q12 import GLSphere

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.panel_1 = wx.Panel(self, -1)
        self.window_1 = GLSphere(self.panel_1)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("Dungeon Crawler")
        self.SetSize((795, 615))
        self.window_1.SetMinSize((11, 18))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(self.window_1, 1, wx.EXPAND, 0)
        self.panel_1.SetAutoLayout(True)
        self.panel_1.SetSizer(sizer_2)
        sizer_2.Fit(self.panel_1)
        sizer_2.SetSizeHints(self.panel_1)
        sizer_1.Add(self.panel_1, 1, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

# end of class MyFrame


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = MyFrame(None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()

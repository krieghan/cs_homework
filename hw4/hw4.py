#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
# generated by wxGlade 0.4.1 on Tue Apr 18 14:20:40 2006

import wx
from ray import GLArena

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.panel_1 = wx.Panel(self, -1)
        self.window_1 = GLArena(self.panel_1)
        self.label_1 = wx.StaticText(self.panel_1, -1, "Local Filename:")
        self.text_ctrl_1 = wx.TextCtrl(self.panel_1, -1, "")
        self.label_2 = wx.StaticText(self.panel_1, -1, "Number of Reflections:")
        self.text_ctrl_2 = wx.TextCtrl(self.panel_1, -1, "")
        self.button_1 = wx.Button(self.panel_1, -1, "Display")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.HandleDisplay, self.button_1)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("Ray Tracer")
        self.SetSize((558, 466))
        self.window_1.SetMinSize((550, 342))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.GridSizer(3, 2, 3, 3)
        sizer_2.Add(self.window_1, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.label_1, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.text_ctrl_1, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.label_2, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.text_ctrl_2, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.button_1, 0, wx.ADJUST_MINSIZE, 0)
        sizer_2.Add(grid_sizer_1, 0, wx.EXPAND, 0)
        self.panel_1.SetAutoLayout(True)
        self.panel_1.SetSizer(sizer_2)
        sizer_2.Fit(self.panel_1)
        sizer_2.SetSizeHints(self.panel_1)
        sizer_1.Add(self.panel_1, 1, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

    def HandleDisplay(self, event): # wxGlade: MyFrame.<event_handler>
        self.window_1.DoDisplay(self.text_ctrl_1.GetValue(), self.text_ctrl_2.GetValue())
        event.Skip()

# end of class MyFrame


class MyApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        frame_1 = MyFrame(None, -1, "")
        self.SetTopWindow(frame_1)
        frame_1.Show()
        return 1

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()

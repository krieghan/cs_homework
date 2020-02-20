#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
# generated by wxGlade 0.4.1 on Mon Apr 03 13:01:10 2006

import wx
from turtle import GLPane

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.panel_1 = wx.Panel(self, -1)
        self.panel_2 = wx.Panel(self.panel_1, -1)
        self.window_1 = GLPane(self.panel_1)
        self.label_1 = wx.StaticText(self.panel_2, -1, "Number of Iterations:")
        self.text_ctrl_1 = wx.TextCtrl(self.panel_2, -1, "")
        self.label_2 = wx.StaticText(self.panel_2, -1, "Seed String:")
        self.text_ctrl_2 = wx.TextCtrl(self.panel_2, -1, "")
        self.label_3 = wx.StaticText(self.panel_2, -1, "Turn Angle:")
        self.text_ctrl_3 = wx.TextCtrl(self.panel_2, -1, "")
        self.label_4 = wx.StaticText(self.panel_2, -1, "F Production: ")
        self.text_ctrl_4 = wx.TextCtrl(self.panel_2, -1, "")
        self.label_5 = wx.StaticText(self.panel_2, -1, "X Production:")
        self.text_ctrl_5 = wx.TextCtrl(self.panel_2, -1, "")
        self.label_6 = wx.StaticText(self.panel_2, -1, "Y Production:")
        self.text_ctrl_6 = wx.TextCtrl(self.panel_2, -1, "")
        self.button_1 = wx.Button(self.panel_2, -1, "Display:")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.Handle_Button, self.button_1)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("frame_1")
        self.SetSize((706, 600))
        self.window_1.SetMinSize((698, 500))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.FlexGridSizer(7, 2, 0, 0)
        sizer_2.Add(self.window_1, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.label_1, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.text_ctrl_1, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.label_2, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.text_ctrl_2, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.label_3, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.text_ctrl_3, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.label_4, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.text_ctrl_4, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.label_5, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.text_ctrl_5, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.label_6, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.text_ctrl_6, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.button_1, 0, wx.ADJUST_MINSIZE, 0)
        self.panel_2.SetAutoLayout(True)
        self.panel_2.SetSizer(grid_sizer_1)
        grid_sizer_1.Fit(self.panel_2)
        grid_sizer_1.SetSizeHints(self.panel_2)
        sizer_2.Add(self.panel_2, 0, wx.EXPAND, 0)
        self.panel_1.SetAutoLayout(True)
        self.panel_1.SetSizer(sizer_2)
        sizer_2.Fit(self.panel_1)
        sizer_2.SetSizeHints(self.panel_1)
        sizer_1.Add(self.panel_1, 1, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade
    
    #Basically, when the button is clicked we want to pass all data to DisplayTurtle.  This will parse it, set up the view and plot the fractal.
    def Handle_Button(self, event): # wxGlade: MyFrame.<event_handler>
        self.window_1.DisplayTurtle(self.text_ctrl_1.GetValue(), self.text_ctrl_2.GetValue(), self.text_ctrl_3.GetValue(), self.text_ctrl_4.GetValue(), self.text_ctrl_5.GetValue(), self.text_ctrl_6.GetValue())
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

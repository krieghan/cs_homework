#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
# generated by wxGlade 0.4.1 on Sun May 14 22:12:29 2006

import wx
from terrain import GLTerrain

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        self.oldvalue = "2"
        # begin wxGlade: MyFrame.__init__        
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.panel_1 = wx.Panel(self, -1)
        self.panel_2 = wx.Panel(self.panel_1, -1)
        self.window_1 = GLTerrain(self.panel_1)
        self.label_1 = wx.StaticText(self.panel_2, -1, "Slide")
        self.label_2 = wx.StaticText(self.panel_2, -1, "Pitch")
        self.label_3 = wx.StaticText(self.panel_2, -1, "Yaw")
        self.label_4 = wx.StaticText(self.panel_2, -1, "Spin")
        self.label_5 = wx.StaticText(self.panel_2, -1, "Grid Size = 2^N + 1")
        self.label_6 = wx.StaticText(self.panel_2, -1, "Skin")
        self.button_4 = wx.Button(self.panel_2, -1, "Increase")
        self.button_5 = wx.Button(self.panel_2, -1, "Decrease")
        self.button_6 = wx.Button(self.panel_2, -1, "Increase")
        self.button_7 = wx.Button(self.panel_2, -1, "Decrease")
        self.button_8 = wx.Button(self.panel_2, -1, "Increase")
        self.button_9 = wx.Button(self.panel_2, -1, "Decrease")
        self.button_10 = wx.Button(self.panel_2, -1, "Increase")
        self.button_11 = wx.Button(self.panel_2, -1, "Decrease")
        self.text_ctrl_1 = wx.TextCtrl(self.panel_2, -1, "2")
        self.button_1 = wx.Button(self.panel_2, -1, "Display")
        self.checkbox_1 = wx.CheckBox(self.panel_2, -1, "")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.IncreaseSlide, self.button_4)
        self.Bind(wx.EVT_BUTTON, self.DecreaseSlide, self.button_5)
        self.Bind(wx.EVT_BUTTON, self.IncreasePitch, self.button_6)
        self.Bind(wx.EVT_BUTTON, self.DecreasePitch, self.button_7)
        self.Bind(wx.EVT_BUTTON, self.IncreaseYaw, self.button_8)
        self.Bind(wx.EVT_BUTTON, self.DecreaseYaw, self.button_9)
        self.Bind(wx.EVT_BUTTON, self.IncreaseSpin, self.button_10)
        self.Bind(wx.EVT_BUTTON, self.DecreaseSpin, self.button_11)
        self.Bind(wx.EVT_BUTTON, self.HandleDisplay, self.button_1)
        self.Bind(wx.EVT_CHECKBOX, self.ChangeSkinMode, self.checkbox_1)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("Terrain Generator")
        self.SetSize((850, 742))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.FlexGridSizer(2, 6, 1, 1)
        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(self.window_1, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.label_1, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.label_2, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.label_3, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.label_4, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.label_5, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.label_6, 0, wx.ADJUST_MINSIZE, 0)
        sizer_3.Add(self.button_4, 0, wx.ADJUST_MINSIZE, 0)
        sizer_3.Add(self.button_5, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(sizer_3, 1, wx.EXPAND, 0)
        sizer_4.Add(self.button_6, 0, wx.ADJUST_MINSIZE, 0)
        sizer_4.Add(self.button_7, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(sizer_4, 1, wx.EXPAND, 0)
        sizer_5.Add(self.button_8, 0, wx.ADJUST_MINSIZE, 0)
        sizer_5.Add(self.button_9, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(sizer_5, 1, wx.EXPAND, 0)
        sizer_6.Add(self.button_10, 0, wx.ADJUST_MINSIZE, 0)
        sizer_6.Add(self.button_11, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(sizer_6, 1, wx.EXPAND, 0)
        sizer_7.Add(self.text_ctrl_1, 0, wx.ADJUST_MINSIZE, 0)
        sizer_7.Add(self.button_1, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(sizer_7, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.checkbox_1, 0, wx.ADJUST_MINSIZE, 0)
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

    def IncreaseSlide(self, event): # wxGlade: MyFrame.<event_handler>
        self.window_1.DoCameraChange(0, -.2)
        event.Skip()

    def DecreaseSlide(self, event): # wxGlade: MyFrame.<event_handler>
        self.window_1.DoCameraChange(0, .2)
        event.Skip()

    def IncreasePitch(self, event): # wxGlade: MyFrame.<event_handler>
        self.window_1.DoCameraChange(1, .2)
        event.Skip()

    def DecreasePitch(self, event): # wxGlade: MyFrame.<event_handler>
        self.window_1.DoCameraChange(1, -.2)
        event.Skip()

    def IncreaseYaw(self, event): # wxGlade: MyFrame.<event_handler>
        self.window_1.DoCameraChange(2, .2)
        event.Skip()

    def DecreaseYaw(self, event): # wxGlade: MyFrame.<event_handler>
        self.window_1.DoCameraChange(2, -.2)
        event.Skip()

    def IncreaseSpin(self, event): # wxGlade: MyFrame.<event_handler>
        self.window_1.AddSpin(.2)
        event.Skip()

    def DecreaseSpin(self, event): # wxGlade: MyFrame.<event_handler>
        self.window_1.AddSpin(-.2)
        event.Skip()

    def ChangeSkinMode(self, event): # wxGlade: MyFrame.<event_handler>
        self.window_1.ChangeSkin()
        event.Skip()

    def HandleDisplay(self, event): # wxGlade: MyFrame.<event_handler>
        newvalue = self.text_ctrl_1.GetValue()
        if self.window_1.DoDisplay(int(newvalue)) == -1:            
            self.text_ctrl_1.SetValue(self.oldvalue)
        self.oldvalue = self.text_ctrl_1.GetValue()
        event.Skip()
        
# end of class MyFrame


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = MyFrame(None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()

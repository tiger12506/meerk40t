import wx

_ = wx.GetTranslation


class UsbConnect(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: UsbConnect.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE | wx.FRAME_TOOL_WINDOW | wx.STAY_ON_TOP
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((915, 424))
        self.usblog_text = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_MULTILINE | wx.TE_WORDWRAP)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade
        self.Bind(wx.EVT_CLOSE, self.on_close, self)
        self.kernel = None
        self.uid = None

    def set_kernel(self, kernel):
        self.kernel = kernel
        try:
            backend = self.kernel.backend
            self.uid = backend.uid
            self.kernel.listen("%s;pipe;device_log" % self.uid, self.update_log)
        except AttributeError:
            pass

    def on_close(self, event):
        self.kernel.unlisten("%s;pipe;device_log" % self.uid, self.update_log)
        self.kernel.mark_window_closed("UsbConnect")
        event.Skip()  # Call destroy as regular.

    def update_log(self, text):
        self.post_update()

    def post_update(self):
        if self.kernel is None:
            return
        try:
            backend = self.kernel.backend
            self.usblog_text.SetValue(backend.device_log)
            self.usblog_text.AppendText("\n")
        except AttributeError:
            return

    def __set_properties(self):
        self.SetTitle(_("UsbConnect"))

    def __do_layout(self):
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(self.usblog_text, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_2)
        self.Layout()

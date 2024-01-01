import wx

from meerk40t.gui.icons import (
    get_default_icon_size,
    icons8_connected,
    icons8_disconnected,
)
from meerk40t.gui.mwindow import MWindow
from meerk40t.kernel import signal_listener

_ = wx.GetTranslation


class SilhouetteControllerPanel(wx.Panel):
    def __init__(self, *args, context=None, **kwds):
        self.service = context
        self.state = "disconnected"
        wx.Panel.__init__(self, *args, **kwds)
        self.SetHelpText("silhouettecontroller")

        self.iconsize = 0.75 * get_default_icon_size()
        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        self.button_device_connect = wx.Button(
            self, wx.ID_ANY, self.button_connect_string("Connection")
        )
        self.button_device_connect.SetBackgroundColour(wx.Colour(102, 255, 102))
        self.button_device_connect.SetToolTip(
            _("Force connection/disconnection from the device.")
        )
        self.button_device_connect.SetBitmap(
            icons8_connected.GetBitmap(use_theme=False, resize=self.iconsize)
        )
        sizer_1.Add(self.button_device_connect, 0, wx.EXPAND, 0)

        static_line = wx.StaticLine(self, wx.ID_ANY)
        sizer_1.Add(static_line, 0, wx.EXPAND, 0)

        self.data_exchange = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_MULTILINE)
        sizer_1.Add(self.data_exchange, 1, wx.EXPAND, 0)

        self.sil_text = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER)
        self.sil_text.SetToolTip(_("Enter a silhuette language command to send it to the laser"))
        self.sil_text.SetFocus()
        sizer_1.Add(self.sil_text, 0, wx.EXPAND, 0)

        self.SetSizer(sizer_1)
        self.Layout()

        self.Bind(wx.EVT_BUTTON, self.on_button_start_connection, self.button_device_connect)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_silcode_enter, self.sil_text)
        self._buffer = ""

    def button_connect_string(self, pattern):
        context = self.service
        if context.interface == "USB":
            return "USB"
        return "Mock"

    def on_button_start_connection(self, event):
        if self.state == "connected":
            self.service.controller.stop()
        else:
            self.service.controller.start()

    def on_silcode_enter(self, event):
        cmd = self.sil_text.GetValue()
        self.service(f"silcode {cmd}")
        self.sil_text.Clear()

    def on_status(self, origin, state):
        self.state = state
        if state in ("uninitialized", "disconnected"):
            self.set_button_state("#ffff00", "Connect", icons8_disconnected)
        elif state == "connected":
            self.set_button_state("#00ff00", "Disconnect", icons8_connected)

    def update(self, data, type):
        if type == "send":
            pass
        elif type == "recv":
            pass
        elif type == "event":
            pass
        elif type == "connection":
            pass
        self._buffer += f"Type: {type}, data: {data}"
        self.service.signal("silhouette_controller_update", True)

    @signal_listener("silhouette_controller_update")
    def update_text_gui(self, origin, *args):
        self.data_exchange.AppendText(self._buffer)

    def pane_show(self):
        if self.state in (None, "uninitialized", "disconnected"):
            self.set_button_state("#ffff00", "Connect", icons8_disconnected)
        elif self.state == "connected":
            self.set_button_state("#00ff00", "Disconnect", icons8_connected)

    def set_button_state(self, color, caption, icon):
        self.button_device_connect.SetBackgroundColour(color)
        self.button_device_connect.SetLabel(self.button_connect_string(caption))
        self.button_device_connect.SetBitmap(
            icon.GetBitmap(use_theme=False, resize=self.iconsize)
        )
        self.button_device_connect.Enable()

    def pane_hide(self):
        return


class SilhouetteController(MWindow):
    def __init__(self, *args, **kwds):
        super().__init__(500, 400, *args, **kwds)
        self.service = self.context.device
        self.SetTitle("Silhouette Controller")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(icons8_connected.GetBitmap())
        self.SetIcon(_icon)

        self.panel = SilhouetteControllerPanel(self, wx.ID_ANY, context=self.service)
        self.Layout()

    @signal_listener("silhouette;status")
    def on_status(self, origin, state):
        self.panel.on_status(origin, state)

    def window_open(self):
        self.service.controller.add_watcher(self.panel.update)
        self.panel.pane_show()

    def window_close(self):
        self.service.controller.remove_watcher(self.panel.update)
        self.panel.pane_hide()

    def delegates(self):
        yield self.panel

    @staticmethod
    def submenu():
        return "Device-Control", "Silhouette Controller"

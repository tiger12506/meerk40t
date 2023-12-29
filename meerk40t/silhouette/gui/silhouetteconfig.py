import wx

from meerk40t.device.gui.defaultactions import DefaultActionPanel
from meerk40t.device.gui.formatterpanel import FormatterPanel
from meerk40t.device.gui.warningpanel import WarningPanel
from meerk40t.gui.choicepropertypanel import ChoicePropertyPanel
from meerk40t.gui.icons import icons8_administrative_tools
from meerk40t.gui.mwindow import MWindow
from meerk40t.gui.wxutils import ScrolledPanel, StaticBoxSizer

_ = wx.GetTranslation

# This class is made by-hand and exists not as a ChoicePropertyPanel because switching
# to a USB radio button choice can show the panel_usb_settings with additional settings
# ChoicePropertyPanel cannot show/hide panel sections
class ConfigurationInterfacePanel(ScrolledPanel):
    def __init__(self, *args, context=None, **kwds):
        kwds["style"] = kwds.get("style", 0)
        ScrolledPanel.__init__(self, *args, **kwds)
        self.context = context

        sizer_page_1 = wx.BoxSizer(wx.VERTICAL)

        sizer_interface = StaticBoxSizer(self, wx.ID_ANY, _("Interface"), wx.VERTICAL)
        sizer_page_1.Add(sizer_interface, 10, wx.EXPAND, 0)

        sizer_interface_radio = wx.BoxSizer(wx.HORIZONTAL)
        sizer_interface.Add(sizer_interface_radio, 0, wx.EXPAND, 0)

        self.radio_usb = wx.RadioButton(
            self, wx.ID_ANY, _("USB"), style=wx.RB_GROUP
        )
        self.radio_usb.SetValue(1)
        self.radio_usb.SetToolTip(
            _(
                "Select this if you have a Silhouette device running through a USB connection."
            )
        )
        sizer_interface_radio.Add(self.radio_usb, 1, wx.EXPAND, 0)

        self.radio_mock = wx.RadioButton(self, wx.ID_ANY, _("Mock"))
        self.radio_mock.SetToolTip(
            _("Select this only for debugging without a physical machine available.")
        )
        sizer_interface_radio.Add(self.radio_mock, 1, wx.EXPAND, 0)

        self.panel_usb_settings = ChoicePropertyPanel(
            self, wx.ID_ANY, context=self.context, choices="usb"
        )

        self.SetSizer(sizer_page_1)
        self.Layout()

        self.Bind(wx.EVT_RADIOBUTTON, self.on_radio_interface, self.radio_usb)
        self.Bind(wx.EVT_RADIOBUTTON, self.on_radio_interface, self.radio_mock)

        if self.context.interface == "usb":
            self.radio_usb.SetValue(True)
        else:
            # Mock
            self.panel_usb_settings.Hide()
            self.radio_mock.SetValue(True)

        self.SetupScrolling()

    def pane_show(self):
        self.panel_usb_settings.pane_show()

    def pane_hide(self):
        self.panel_usb_settings.pane_hide()

    def on_radio_interface(self, event):
        try:
            if self.radio_usb.GetValue():
                self.context.interface = "usb"
                self.context.signal("update_interface")
                self.panel_usb_settings.Show()
        except AttributeError:
            pass
        if self.radio_mock.GetValue():
            self.panel_usb_settings.Hide()
            self.context.interface = "mock"
            self.context.signal("update_interface")
        self.Layout()


class SilhouetteConfig(MWindow):
    def __init__(self, *args, **kwds):
        super().__init__(345, 415, *args, **kwds)
        self.context = self.context.device
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(icons8_administrative_tools.GetBitmap())
        self.SetIcon(_icon)
        self.SetTitle(_("Silhouette-Configuration"))

        self.notebook_main = wx.aui.AuiNotebook(
            self,
            -1,
            style=wx.aui.AUI_NB_TAB_EXTERNAL_MOVE
            | wx.aui.AUI_NB_SCROLL_BUTTONS
            | wx.aui.AUI_NB_TAB_SPLIT
            | wx.aui.AUI_NB_TAB_MOVE,
        )
        self.panels = []
        self._requested_status = False

        panel_device = ChoicePropertyPanel(
            self, wx.ID_ANY, context=self.context, choices="bed_dim",
        )

        panel_interface = ConfigurationInterfacePanel(
            self.notebook_main, wx.ID_ANY, context=self.context,
        )

        panel_adv = ChoicePropertyPanel(
            self, wx.ID_ANY, context=self.context, choices="silhouette-adv"
        )

        panel_warn = WarningPanel(self, id=wx.ID_ANY, context=self.context)
        panel_actions = DefaultActionPanel(self, id=wx.ID_ANY, context=self.context)
        panel_formatter = FormatterPanel(self, id=wx.ID_ANY, context=self.context)

        self.panels.append(panel_device)
        self.panels.append(panel_interface)
        self.panels.append(panel_adv)
        self.panels.append(panel_warn)
        self.panels.append(panel_actions)
        self.panels.append(panel_formatter)

        self.notebook_main.AddPage(panel_device, _("Device"))
        self.notebook_main.AddPage(panel_interface, _("Interface"))
        self.notebook_main.AddPage(panel_adv, _("Advanced"))
        self.notebook_main.AddPage(panel_warn, _("Warning"))
        self.notebook_main.AddPage(panel_actions, _("Default Actions"))
        self.notebook_main.AddPage(panel_formatter, _("Display Options"))
        self.Layout()
        for panel in self.panels:
            self.add_module_delegate(panel)

    def window_open(self):
        for panel in self.panels:
            panel.pane_show()

    def window_close(self):
        for panel in self.panels:
            panel.pane_hide()

    def window_preserve(self):
        return False

    @staticmethod
    def submenu():
        return "Device-Settings", "Silhouette-Configuration"

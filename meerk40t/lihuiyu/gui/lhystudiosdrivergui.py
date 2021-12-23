# -*- coding: ISO-8859-1 -*-

import wx

from meerk40t.gui.icons import icons8_administrative_tools_50
from meerk40t.gui.mwindow import MWindow

_ = wx.GetTranslation


class LhystudiosConfigurationPanel(wx.Panel):
    def __init__(self, *args, context=None, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)

        sizer_main = wx.BoxSizer(wx.HORIZONTAL)

        sizer_page_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_main.Add(sizer_page_1, 0, wx.EXPAND, 0)

        sizer_config = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Configuration"), wx.HORIZONTAL)
        sizer_page_1.Add(sizer_config, 0, wx.EXPAND, 0)

        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_config.Add(sizer_3, 1, wx.EXPAND, 0)

        sizer_board = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Board Setup"), wx.HORIZONTAL)
        sizer_3.Add(sizer_board, 0, wx.EXPAND, 0)

        self.context = context.device
        self.Bind(
            wx.EVT_KEY_DOWN,
            lambda e: self.context.console("webhelp help\n")
            if e.GetKeyCode() == wx.WXK_F1
            else None,
            self,
        )

        self.combobox_board = wx.ComboBox(self, wx.ID_ANY, choices=["M2", "B2", "M", "M1", "A", "B", "B1"], style=wx.CB_DROPDOWN)
        self.combobox_board.SetToolTip("Select the board to use. This has an effects the speedcodes used.")
        self.combobox_board.SetSelection(0)
        sizer_board.Add(self.combobox_board, 1, wx.EXPAND, 0)

        self.checkbox_swap_xy = wx.CheckBox(self, wx.ID_ANY, "Swap X and Y")
        self.checkbox_swap_xy.SetToolTip("Swaps the X and Y axis. This happens before the FlipX and FlipY.")
        sizer_3.Add(self.checkbox_swap_xy, 0, 0, 0)

        sizer_17 = wx.BoxSizer(wx.VERTICAL)
        sizer_config.Add(sizer_17, 1, wx.EXPAND, 0)

        self.checkbox_flip_x = wx.CheckBox(self, wx.ID_ANY, "Flip X")
        self.checkbox_flip_x.SetToolTip("Flip the Right and Left commands sent to the controller")
        sizer_17.Add(self.checkbox_flip_x, 0, 0, 0)

        self.checkbox_home_right = wx.CheckBox(self, wx.ID_ANY, "Home Right")
        self.checkbox_home_right.SetToolTip("Indicates the device Home is on the right")
        sizer_17.Add(self.checkbox_home_right, 0, 0, 0)

        sizer_16 = wx.BoxSizer(wx.VERTICAL)
        sizer_config.Add(sizer_16, 1, wx.EXPAND, 0)

        self.checkbox_flip_y = wx.CheckBox(self, wx.ID_ANY, "Flip Y")
        self.checkbox_flip_y.SetToolTip("Flip the Top and Bottom commands sent to the controller")
        sizer_16.Add(self.checkbox_flip_y, 0, 0, 0)

        self.checkbox_home_bottom = wx.CheckBox(self, wx.ID_ANY, "Home Bottom")
        self.checkbox_home_bottom.SetToolTip("Indicates the device Home is on the bottom")
        sizer_16.Add(self.checkbox_home_bottom, 0, 0, 0)

        sizer_interface = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Interface"), wx.VERTICAL)
        sizer_page_1.Add(sizer_interface, 0, wx.EXPAND, 0)

        sizer_interface_radio = wx.BoxSizer(wx.VERTICAL)
        sizer_interface.Add(sizer_interface_radio, 0, wx.EXPAND, 0)

        self.radio_usb = wx.RadioButton(self, wx.ID_ANY, "USB", style=wx.RB_GROUP)
        self.radio_usb.SetValue(1)
        sizer_interface_radio.Add(self.radio_usb, 0, 0, 0)

        self.radio_tcp = wx.RadioButton(self, wx.ID_ANY, "Networked")
        sizer_interface_radio.Add(self.radio_tcp, 0, 0, 0)

        self.radio_mock = wx.RadioButton(self, wx.ID_ANY, "Mock")
        self.radio_mock.SetToolTip("DEBUG. Without a K40 connected continue to process things as if there was one.")
        sizer_interface_radio.Add(self.radio_mock, 0, 0, 0)

        sizer_usb_settings = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "USB Settings"), wx.VERTICAL)
        sizer_interface.Add(sizer_usb_settings, 0, wx.EXPAND, 0)

        sizer_usb_restrict = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "USB Connection Restrictions"), wx.HORIZONTAL)
        sizer_usb_settings.Add(sizer_usb_restrict, 0, wx.EXPAND, 0)

        sizer_26 = wx.BoxSizer(wx.VERTICAL)
        sizer_usb_restrict.Add(sizer_26, 0, wx.EXPAND, 0)

        sizer_12 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Chip Version"), wx.HORIZONTAL)
        sizer_26.Add(sizer_12, 0, wx.EXPAND, 0)

        self.text_device_version = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)
        self.text_device_version.SetMinSize((55, 23))
        sizer_12.Add(self.text_device_version, 0, 0, 0)

        self.spin_device_version = wx.SpinCtrl(self, wx.ID_ANY, "-1", min=-1, max=25)
        self.spin_device_version.SetMinSize((40, 23))
        self.spin_device_version.SetToolTip("-1 match anything. 0-255 match exactly that value.")
        sizer_12.Add(self.spin_device_version, 0, 0, 0)

        sizer_6 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Device Index:"), wx.HORIZONTAL)
        sizer_26.Add(sizer_6, 0, wx.EXPAND, 0)

        self.text_device_index = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)
        self.text_device_index.SetMinSize((55, 23))
        sizer_6.Add(self.text_device_index, 0, 0, 0)

        self.spin_device_index = wx.SpinCtrl(self, wx.ID_ANY, "-1", min=-1, max=5)
        self.spin_device_index.SetMinSize((40, 23))
        self.spin_device_index.SetToolTip("-1 match anything. 0-5 match exactly that value.")
        sizer_6.Add(self.spin_device_index, 0, 0, 0)

        sizer_27 = wx.BoxSizer(wx.VERTICAL)
        sizer_usb_restrict.Add(sizer_27, 0, wx.EXPAND, 0)

        sizer_10 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Device Address:"), wx.HORIZONTAL)
        sizer_27.Add(sizer_10, 0, wx.EXPAND, 0)

        self.text_device_address = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)
        self.text_device_address.SetMinSize((55, 23))
        sizer_10.Add(self.text_device_address, 0, 0, 0)

        self.spin_device_address = wx.SpinCtrl(self, wx.ID_ANY, "-1", min=-1, max=5)
        self.spin_device_address.SetMinSize((40, 23))
        self.spin_device_address.SetToolTip("-1 match anything. 0-5 match exactly that value.")
        sizer_10.Add(self.spin_device_address, 0, 0, 0)

        sizer_11 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Device Bus:"), wx.HORIZONTAL)
        sizer_27.Add(sizer_11, 0, wx.EXPAND, 0)

        self.text_device_bus = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)
        self.text_device_bus.SetMinSize((55, 23))
        sizer_11.Add(self.text_device_bus, 0, 0, 0)

        self.spin_device_bus = wx.SpinCtrl(self, wx.ID_ANY, "-1", min=-1, max=5)
        self.spin_device_bus.SetMinSize((40, 23))
        self.spin_device_bus.SetToolTip("-1 match anything. 0-5 match exactly that value.")
        sizer_11.Add(self.spin_device_bus, 0, 0, 0)

        sizer_13 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "TCP Settings"), wx.HORIZONTAL)
        sizer_interface.Add(sizer_13, 0, wx.EXPAND, 0)

        sizer_21 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Address"), wx.VERTICAL)
        sizer_13.Add(sizer_21, 0, 0, 0)

        self.text_device = wx.TextCtrl(self, wx.ID_ANY, "")
        self.text_device.SetMinSize((150, 23))
        self.text_device.SetToolTip("IP/Host if the server computer")
        sizer_21.Add(self.text_device, 0, 0, 0)

        sizer_port = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Port"), wx.VERTICAL)
        sizer_13.Add(sizer_port, 0, 0, 0)

        self.text_location = wx.TextCtrl(self, wx.ID_ANY, "")
        self.text_location.SetToolTip("Port for tcp connection on the server computer")
        sizer_port.Add(self.text_location, 0, wx.EXPAND, 0)

        sizer_serial = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Serial Number"), wx.HORIZONTAL)
        sizer_page_1.Add(sizer_serial, 0, wx.EXPAND, 0)

        sizer_9 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_serial.Add(sizer_9, 1, wx.EXPAND, 0)

        self.checkbox_2 = wx.CheckBox(self, wx.ID_ANY, "Require Serial Number")
        self.checkbox_2.SetToolTip("Require a serial number match for this board")
        sizer_9.Add(self.checkbox_2, 0, 0, 0)

        self.text_serial_number = wx.TextCtrl(self, wx.ID_ANY, "")
        self.text_serial_number.SetMinSize((150, 23))
        self.text_serial_number.SetToolTip("Board Serial Number to be used to identify a specific laser. If the device fails to match the serial number it will be disconnected.")
        sizer_9.Add(self.text_serial_number, 0, wx.EXPAND, 0)

        sizer_8 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Rapid Jog"), wx.HORIZONTAL)
        sizer_page_1.Add(sizer_8, 0, wx.EXPAND, 0)

        sizer_23 = wx.BoxSizer(wx.VERTICAL)
        sizer_8.Add(sizer_23, 1, wx.EXPAND, 0)

        self.check_rapid_moves_between = wx.CheckBox(self, wx.ID_ANY, "Rapid Moves Between Objects")
        self.check_rapid_moves_between.SetToolTip("Perform rapid moves between the objects")
        self.check_rapid_moves_between.SetValue(1)
        sizer_23.Add(self.check_rapid_moves_between, 0, 0, 0)

        sizer_25 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Minimum Jog Distance"), wx.HORIZONTAL)
        sizer_23.Add(sizer_25, 1, 0, 0)

        self.text_minimum_jog_distance = wx.TextCtrl(self, wx.ID_ANY, "")
        sizer_25.Add(self.text_minimum_jog_distance, 0, 0, 0)

        self.radio_box_1 = wx.RadioBox(self, wx.ID_ANY, "Jog Method", choices=["Default", "Reset", "Finish"], majorDimension=3, style=wx.RA_SPECIFY_ROWS)
        self.radio_box_1.SetSelection(0)
        sizer_8.Add(self.radio_box_1, 0, 0, 0)

        sizer_page_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_main.Add(sizer_page_2, 0, wx.EXPAND, 0)

        sizer_buffer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Write Buffer"), wx.HORIZONTAL)
        sizer_page_2.Add(sizer_buffer, 0, wx.EXPAND, 0)

        self.checkbox_limit_buffer = wx.CheckBox(self, wx.ID_ANY, "Limit Write Buffer")
        self.checkbox_limit_buffer.SetToolTip("Limit the write buffer to a certain amount. Permits on-the-fly command production.")
        self.checkbox_limit_buffer.SetValue(1)
        sizer_buffer.Add(self.checkbox_limit_buffer, 0, 0, 0)

        self.text_buffer_length = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)
        self.text_buffer_length.SetToolTip("Current number of bytes in the write buffer.")
        sizer_buffer.Add(self.text_buffer_length, 0, 0, 0)

        label_14 = wx.StaticText(self, wx.ID_ANY, "/")
        sizer_buffer.Add(label_14, 0, 0, 0)

        self.spin_packet_buffer_max = wx.SpinCtrl(self, wx.ID_ANY, "1500", min=1, max=1000000)
        self.spin_packet_buffer_max.SetToolTip("Current maximum write buffer limit.")
        sizer_buffer.Add(self.spin_packet_buffer_max, 0, 0, 0)

        sizer_general = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "General Options"), wx.VERTICAL)
        sizer_page_2.Add(sizer_general, 0, wx.EXPAND, 0)

        self.checkbox_autolock = wx.CheckBox(self, wx.ID_ANY, "Automatically lock rail")
        self.checkbox_autolock.SetToolTip("Lock rail after operations are finished.")
        self.checkbox_autolock.SetValue(1)
        sizer_general.Add(self.checkbox_autolock, 0, 0, 0)

        self.checkbox_plot_shift = wx.CheckBox(self, wx.ID_ANY, "Pulse Shifting")
        self.checkbox_plot_shift.SetToolTip("During the pulse planning process allow shifting pulses by one unit to increase command efficiency\nThis may prevent device stutter and reduce pulse accuracy by one up to one unit.")
        sizer_general.Add(self.checkbox_plot_shift, 1, 0, 0)

        self.checkbox_random_ppi = wx.CheckBox(self, wx.ID_ANY, "Randomize PPI")
        self.checkbox_random_ppi.SetToolTip("Rather than orderly PPI, we perform PPI based on a randomized average")
        self.checkbox_random_ppi.Enable(False)
        sizer_general.Add(self.checkbox_random_ppi, 0, 0, 0)

        self.checkbox_fix_speeds = wx.CheckBox(self, wx.ID_ANY, "Fix rated to actual speed")
        self.checkbox_fix_speeds.SetToolTip("Correct for speed invalidity. Lhystudios speeds are 92% of the correctly rated speed.")
        sizer_general.Add(self.checkbox_fix_speeds, 0, 0, 0)

        self.checkbox_strict = wx.CheckBox(self, wx.ID_ANY, "Strict")
        self.checkbox_strict.SetToolTip("Forces the device to enter and exit programmed speed mode from the same direction.\nThis may prevent devices like the M2-V4 and earlier from having issues. Not typically needed.")
        sizer_general.Add(self.checkbox_strict, 0, 0, 0)

        self.checkbox_alternative_raster = wx.CheckBox(self, wx.ID_ANY, "Alt Raster Style")
        sizer_general.Add(self.checkbox_alternative_raster, 0, 0, 0)

        self.checkbox_twitchless = wx.CheckBox(self, wx.ID_ANY, "Twitchless Vectors")
        sizer_general.Add(self.checkbox_twitchless, 0, 0, 0)

        sizer_home = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Shift Home Position"), wx.VERTICAL)
        sizer_page_2.Add(sizer_home, 0, wx.EXPAND, 0)

        sizer_4 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "X:"), wx.HORIZONTAL)
        sizer_home.Add(sizer_4, 2, wx.EXPAND, 0)

        self.spin_home_x = wx.SpinCtrlDouble(self, wx.ID_ANY, "0.0", min=-50000.0, max=50000.0)
        self.spin_home_x.SetMinSize((80, 23))
        self.spin_home_x.SetToolTip("Translate Home X")
        sizer_4.Add(self.spin_home_x, 0, 0, 0)

        label_12 = wx.StaticText(self, wx.ID_ANY, "steps")
        sizer_4.Add(label_12, 0, 0, 0)

        sizer_2 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Y:"), wx.HORIZONTAL)
        sizer_home.Add(sizer_2, 2, wx.EXPAND, 0)

        self.spin_home_y = wx.SpinCtrlDouble(self, wx.ID_ANY, "0.0", min=-50000.0, max=50000.0)
        self.spin_home_y.SetMinSize((80, 23))
        self.spin_home_y.SetToolTip("Translate Home Y")
        sizer_2.Add(self.spin_home_y, 0, 0, 0)

        label_11 = wx.StaticText(self, wx.ID_ANY, "steps")
        sizer_2.Add(label_11, 0, 0, 0)

        self.button_home_by_current = wx.Button(self, wx.ID_ANY, "Set Current")
        self.button_home_by_current.SetToolTip("Set Home Position based on the current position")
        sizer_home.Add(self.button_home_by_current, 1, 0, 0)

        sizer_bed = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Bed Dimensions"), wx.HORIZONTAL)
        sizer_page_2.Add(sizer_bed, 0, wx.EXPAND, 0)

        sizer_14 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Width"), wx.HORIZONTAL)
        sizer_bed.Add(sizer_14, 1, 0, 0)

        self.spin_bedwidth = wx.SpinCtrlDouble(self, wx.ID_ANY, "12205.0", min=1.0, max=100000.0)
        self.spin_bedwidth.SetMinSize((80, 23))
        self.spin_bedwidth.SetToolTip("Width of the laser bed.")
        self.spin_bedwidth.SetIncrement(40.0)
        sizer_14.Add(self.spin_bedwidth, 4, 0, 0)

        label_17 = wx.StaticText(self, wx.ID_ANY, "steps")
        sizer_14.Add(label_17, 1, 0, 0)

        sizer_15 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Height"), wx.HORIZONTAL)
        sizer_bed.Add(sizer_15, 1, 0, 0)

        label_3 = wx.StaticText(self, wx.ID_ANY, "")
        sizer_15.Add(label_3, 0, 0, 0)

        self.spin_bedheight = wx.SpinCtrlDouble(self, wx.ID_ANY, "8268.0", min=1.0, max=100000.0)
        self.spin_bedheight.SetMinSize((80, 23))
        self.spin_bedheight.SetToolTip("Height of the laser bed.")
        self.spin_bedheight.SetIncrement(40.0)
        sizer_15.Add(self.spin_bedheight, 4, 0, 0)

        label_18 = wx.StaticText(self, wx.ID_ANY, "steps\n")
        sizer_15.Add(label_18, 1, 0, 0)

        sizer_scale_factors = wx.BoxSizer(wx.HORIZONTAL)
        sizer_page_2.Add(sizer_scale_factors, 0, wx.EXPAND, 0)

        sizer_19 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "X Scale Factor"), wx.HORIZONTAL)
        sizer_scale_factors.Add(sizer_19, 0, wx.EXPAND, 0)

        self.text_scale_x = wx.TextCtrl(self, wx.ID_ANY, "1.000")
        self.text_scale_x.SetToolTip("Scale factor for the X-axis. This defines the ratio of mils to steps. This is usually at 1:1 steps/mils but due to functional issues it can deviate and needs to be accounted for")
        sizer_19.Add(self.text_scale_x, 0, 0, 0)

        sizer_20 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Y Scale Factor"), wx.HORIZONTAL)
        sizer_scale_factors.Add(sizer_20, 0, wx.EXPAND, 0)

        self.text_scale_y = wx.TextCtrl(self, wx.ID_ANY, "1.000")
        self.text_scale_y.SetToolTip("Scale factor for the Y-axis. This defines the ratio of mils to steps. This is usually at 1:1 steps/mils but due to functional issues it can deviate and needs to be accounted for")
        sizer_20.Add(self.text_scale_y, 0, 0, 0)

        self.SetSizer(sizer_main)

        self.Layout()

        self.Bind(wx.EVT_COMBOBOX, self.on_combobox_boardtype, self.combobox_board)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_swapxy, self.checkbox_swap_xy)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_flip_x, self.checkbox_flip_x)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_home_right, self.checkbox_home_right)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_flip_y, self.checkbox_flip_y)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_home_bottom, self.checkbox_home_bottom)
        self.Bind(wx.EVT_RADIOBUTTON, self.on_radio_interface, self.radio_usb)
        self.Bind(wx.EVT_RADIOBUTTON, self.on_radio_interface, self.radio_tcp)
        self.Bind(wx.EVT_RADIOBUTTON, self.on_radio_interface, self.radio_mock)
        self.Bind(wx.EVT_SPINCTRL, self.spin_on_device_version, self.spin_device_version)
        self.Bind(wx.EVT_TEXT_ENTER, self.spin_on_device_version, self.spin_device_version)
        self.Bind(wx.EVT_SPINCTRL, self.spin_on_device_index, self.spin_device_index)
        self.Bind(wx.EVT_TEXT_ENTER, self.spin_on_device_index, self.spin_device_index)
        self.Bind(wx.EVT_SPINCTRL, self.spin_on_device_address, self.spin_device_address)
        self.Bind(wx.EVT_TEXT_ENTER, self.spin_on_device_address, self.spin_device_address)
        self.Bind(wx.EVT_SPINCTRL, self.spin_on_device_bus, self.spin_device_bus)
        self.Bind(wx.EVT_TEXT_ENTER, self.spin_on_device_bus, self.spin_device_bus)
        self.Bind(wx.EVT_TEXT, self.on_text_address, self.text_device)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_text_address, self.text_device)
        self.Bind(wx.EVT_TEXT, self.on_text_port, self.text_location)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_text_port, self.text_location)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_rapid_between, self.check_rapid_moves_between)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_limit_packet_buffer, self.checkbox_limit_buffer)
        self.Bind(wx.EVT_SPINCTRL, self.on_spin_packet_buffer_max, self.spin_packet_buffer_max)
        self.Bind(wx.EVT_TEXT, self.on_spin_packet_buffer_max, self.spin_packet_buffer_max)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_spin_packet_buffer_max, self.spin_packet_buffer_max)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_autolock, self.checkbox_autolock)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_pulse_shift, self.checkbox_plot_shift)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_random_ppi, self.checkbox_random_ppi)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_fix_speeds, self.checkbox_fix_speeds)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_strict, self.checkbox_strict)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_alt_raster, self.checkbox_alternative_raster)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_twitchless, self.checkbox_twitchless)
        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.spin_on_home_x, self.spin_home_x)
        self.Bind(wx.EVT_TEXT_ENTER, self.spin_on_home_x, self.spin_home_x)
        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.spin_on_home_y, self.spin_home_y)
        self.Bind(wx.EVT_TEXT_ENTER, self.spin_on_home_y, self.spin_home_y)
        self.Bind(wx.EVT_BUTTON, self.on_button_set_home_current, self.button_home_by_current)
        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.spin_on_bedwidth, self.spin_bedwidth)
        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.spin_on_bedheight, self.spin_bedheight)
        self.Bind(wx.EVT_TEXT, self.on_text_x_scale, self.text_scale_x)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_text_x_scale, self.text_scale_x)
        self.Bind(wx.EVT_TEXT, self.on_text_y_scale, self.text_scale_y)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_text_y_scale, self.text_scale_y)

        # end wxGlade
        context = self.context
        context.setting(bool, "fix_speeds", False)
        context.setting(bool, "swap_xy", False)
        context.setting(bool, "flip_x", False)
        context.setting(bool, "flip_y", False)
        context.setting(bool, "home_right", False)
        context.setting(bool, "home_bottom", False)
        context.setting(bool, "strict", False)

        context.setting(int, "home_adjust_x", 0)
        context.setting(int, "home_adjust_y", 0)
        context.setting(bool, "autolock", True)
        context.setting(str, "board", "M2")
        context.setting(bool, "buffer_limit", True)
        context.setting(int, "buffer_max", 1500)
        context.setting(bool, "random_ppi", False)
        context.setting(bool, "plot_shift", False)
        context.setting(bool, "raster_accel_table", False)
        context.setting(bool, "vector_accel_table", False)

        self.checkbox_fix_speeds.SetValue(context.fix_speeds)
        self.radio_mock.SetValue(context.networked)
        self.checkbox_swap_xy.SetValue(context.swap_xy)
        self.checkbox_flip_x.SetValue(context.flip_x)
        self.checkbox_flip_y.SetValue(context.flip_y)
        self.checkbox_home_right.SetValue(context.home_right)
        self.checkbox_home_bottom.SetValue(context.home_bottom)
        self.checkbox_strict.SetValue(context.strict)

        self.spin_home_x.SetValue(context.home_adjust_x)
        self.spin_home_y.SetValue(context.home_adjust_y)
        self.checkbox_autolock.SetValue(context.autolock)
        self.combobox_board.SetValue(context.board)
        self.checkbox_limit_buffer.SetValue(context.buffer_limit)
        self.spin_packet_buffer_max.SetValue(context.buffer_max)

        self.checkbox_random_ppi.SetValue(context.random_ppi)
        self.checkbox_plot_shift.SetValue(context.plot_shift)

    def __set_properties(self):
        self.combobox_board.SetToolTip(
            _("Select the board to use. This has an effects the speedcodes used.")
        )
        self.combobox_board.SetSelection(0)
        self.checkbox_fix_speeds.SetToolTip(
            _(
                "Correct for speed invalidity. Lhystudios speeds are 92% of the correctly rated speed."
            )
        )
        self.checkbox_networked.SetToolTip(
            _(
                "Run this device as a networked device. This requires a lhyserver located on the address specified.\nThe M2Nano does not natively provide any network capabilities."
            )
        )
        self.checkbox_flip_x.SetToolTip(
            _("Flip the Right and Left commands sent to the controller")
        )
        self.checkbox_home_right.SetToolTip(
            _("Indicates the device Home is on the right")
        )
        self.checkbox_flip_y.SetToolTip(
            _("Flip the Top and Bottom commands sent to the controller")
        )
        self.checkbox_home_bottom.SetToolTip(
            _("Indicates the device Home is on the bottom")
        )
        self.checkbox_swap_xy.SetToolTip(
            _("Swaps the X and Y axis. This happens before the FlipX and FlipY.")
        )
        self.checkbox_strict.SetToolTip(
            _(
                "Forces the device to enter and exit programmed speed mode from the same direction.\nThis may prevent devices like the M2-V4 and earlier from having issues. Not typically needed."
            )
        )
        self.spin_home_x.SetMinSize((80, 23))
        self.spin_home_x.SetToolTip(_("Translate Home X"))
        self.spin_home_y.SetMinSize((80, 23))
        self.spin_home_y.SetToolTip(_("Translate Home Y"))
        self.button_home_by_current.SetToolTip(
            _("Set Home Position based on the current position")
        )
        self.checkbox_plot_shift.SetToolTip(
            "\n".join(
                (
                    _(
                        "Pulse Grouping is an alternative means of reducing the incidence of stuttering, allowing you potentially to burn at higher speeds."
                    ),
                    _(
                        "This setting is a global equivalent to the Pulse Grouping option in Operation Properties."
                    ),
                    _(
                        "It works by swapping adjacent on or off bits to group on and off together and reduce the number of switches."
                    ),
                    _(
                        'As an example, instead of 1010 it will burn 1100 - because the laser beam is overlapping, and because a bit is only moved at most 1/1000", the difference should not be visible even under magnification.'
                    ),
                    _(
                        "Whilst the Pulse Grouping option in Operations are set for that operation before the job is spooled, and cannot be changed on the fly,"
                    )
                    + " "
                    + _(
                        "this global Pulse Grouping option is checked as instructions are sent to the laser and can turned on and off during the burn process."
                    ),
                    _(
                        "Because the changes are believed to be small enough to be undetectable, you may wish to leave this permanently checked."
                    ),
                )
            )
        )
        self.checkbox_random_ppi.SetToolTip(
            _("Rather than orderly PPI, we perform PPI based on a randomized average")
        )
        self.checkbox_random_ppi.Enable(False)
        self.checkbox_limit_buffer.SetToolTip(
            _(
                "Limit the write buffer to a certain amount. Permits on-the-fly command production."
            )
        )
        self.checkbox_limit_buffer.SetValue(1)
        self.text_buffer_length.SetToolTip(
            _("Current number of bytes in the write buffer.")
        )
        self.spin_packet_buffer_max.SetToolTip(_("Current maximum write buffer limit."))
        self.checkbox_autolock.SetToolTip(_("Lock rail after operations are finished."))
        self.checkbox_autolock.SetValue(1)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: LhystudiosDriver.__do_layout
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_general = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("General Options:")), wx.HORIZONTAL
        )
        sizer_buffer = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Write Buffer:")), wx.HORIZONTAL
        )
        sizer_6 = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Pulse Planner:")), wx.HORIZONTAL
        )
        sizer_home = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Shift Home Position:")), wx.HORIZONTAL
        )
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_config = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Configuration:")), wx.HORIZONTAL
        )
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_16 = wx.BoxSizer(wx.VERTICAL)
        sizer_17 = wx.BoxSizer(wx.VERTICAL)
        sizer_board = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Board Setup:")), wx.HORIZONTAL
        )
        sizer_board.Add(self.combobox_board, 1, 0, 0)
        label_1 = wx.StaticText(self, wx.ID_ANY, "")
        sizer_board.Add(label_1, 1, 0, 0)
        sizer_board.Add(self.checkbox_fix_speeds, 0, 0, 0)
        sizer_board.Add(self.checkbox_networked, 0, 0, 0)
        sizer_main.Add(sizer_board, 1, wx.EXPAND, 0)
        sizer_17.Add(self.checkbox_flip_x, 0, 0, 0)
        sizer_17.Add(self.checkbox_home_right, 0, 0, 0)
        sizer_config.Add(sizer_17, 1, wx.EXPAND, 0)
        sizer_16.Add(self.checkbox_flip_y, 0, 0, 0)
        sizer_16.Add(self.checkbox_home_bottom, 0, 0, 0)
        sizer_config.Add(sizer_16, 1, wx.EXPAND, 0)
        sizer_3.Add(self.checkbox_swap_xy, 0, 0, 0)
        sizer_3.Add(self.checkbox_strict, 0, 0, 0)
        sizer_config.Add(sizer_3, 1, wx.EXPAND, 0)
        sizer_main.Add(sizer_config, 1, wx.EXPAND, 0)
        label_9 = wx.StaticText(self, wx.ID_ANY, "X")
        sizer_4.Add(label_9, 0, 0, 0)
        sizer_4.Add(self.spin_home_x, 0, 0, 0)
        label_12 = wx.StaticText(self, wx.ID_ANY, _("mil"))
        sizer_4.Add(label_12, 0, 0, 0)
        sizer_home.Add(sizer_4, 2, wx.EXPAND, 0)
        label_10 = wx.StaticText(self, wx.ID_ANY, "Y")
        sizer_2.Add(label_10, 0, 0, 0)
        sizer_2.Add(self.spin_home_y, 0, 0, 0)
        label_11 = wx.StaticText(self, wx.ID_ANY, _("mil"))
        sizer_2.Add(label_11, 1, 0, 0)
        sizer_home.Add(sizer_2, 2, wx.EXPAND, 0)
        sizer_home.Add(self.button_home_by_current, 1, 0, 0)
        sizer_main.Add(sizer_home, 1, wx.EXPAND, 0)
        sizer_6.Add(self.checkbox_plot_shift, 1, 0, 0)
        sizer_6.Add(self.checkbox_random_ppi, 0, 0, 0)
        sizer_main.Add(sizer_6, 1, wx.EXPAND, 0)
        sizer_buffer.Add(self.checkbox_limit_buffer, 1, 0, 0)
        sizer_buffer.Add(self.text_buffer_length, 1, 0, 0)
        label_14 = wx.StaticText(self, wx.ID_ANY, "/")
        sizer_buffer.Add(label_14, 0, 0, 0)
        sizer_buffer.Add(self.spin_packet_buffer_max, 1, 0, 0)
        sizer_main.Add(sizer_buffer, 0, 0, 0)
        sizer_general.Add(self.checkbox_autolock, 0, 0, 0)
        sizer_main.Add(sizer_general, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_main)
        self.Layout()
        # end wxGlade

    def pane_show(self):
        self.context.listen("pipe;buffer", self.on_buffer_update)
        self.context.listen("active", self.on_active_change)
        self.checkbox_flip_x.SetFocus()

    def pane_hide(self):
        self.context.unlisten("pipe;buffer", self.on_buffer_update)
        self.context.unlisten("active", self.on_active_change)

    def on_active_change(self, origin, active):
        # self.Close()
        pass

    def calc_home_position(self):
        x = 0
        y = 0
        if self.context.home_right:
            x = int(self.context.device.bedwidth)
        if self.context.home_bottom:
            y = int(self.context.device.bedheight)
        return x, y

    def on_combobox_boardtype(self, event=None):
        self.context.board = self.combobox_board.GetValue()

    def on_check_swapxy(self, event=None):
        self.context.swap_xy = self.checkbox_swap_xy.GetValue()
        self.context("code_update\n")

    def on_check_fix_speeds(self, event=None):
        self.context.fix_speeds = self.checkbox_fix_speeds.GetValue()

    def on_check_networked(self, event=None):
        self.context.networked = self.checkbox_networked.GetValue()
        self.context("network_update\n")
        self.context.signal("network_update")

    def on_check_strict(self, event=None):
        self.context.strict = self.checkbox_strict.GetValue()

    def on_check_flip_x(self, event=None):
        self.context.flip_x = self.checkbox_flip_x.GetValue()
        self.context("code_update\n")

    def on_check_home_right(self, event=None):
        self.context.home_right = self.checkbox_home_right.GetValue()

    def on_check_flip_y(self, event=None):
        self.context.flip_y = self.checkbox_flip_y.GetValue()
        self.context("code_update\n")

    def on_check_home_bottom(self, event=None):
        self.context.home_bottom = self.checkbox_home_bottom.GetValue()

    def spin_on_home_x(self, event=None):
        self.context.home_adjust_x = int(self.spin_home_x.GetValue())

    def spin_on_home_y(self, event=None):
        self.context.home_adjust_y = int(self.spin_home_y.GetValue())

    def on_button_set_home_current(self, event=None):
        x, y = self.calc_home_position()
        current_x = self.context.device.current_x - x
        current_y = self.context.device.current_y - y
        self.context.home_adjust_x = int(current_x)
        self.context.home_adjust_y = int(current_y)
        self.spin_home_x.SetValue(self.context.home_adjust_x)
        self.spin_home_y.SetValue(self.context.home_adjust_y)

    def on_check_autolock(self, event=None):
        self.context.autolock = self.checkbox_autolock.GetValue()

    def on_check_limit_packet_buffer(
        self, event=None
    ):  # wxGlade: JobInfo.<event_handler>
        self.context.buffer_limit = self.checkbox_limit_buffer.GetValue()

    def on_spin_packet_buffer_max(self, event=None):  # wxGlade: JobInfo.<event_handler>
        self.context.buffer_max = self.spin_packet_buffer_max.GetValue()

    def on_check_pulse_shift(
        self, event=None
    ):  # wxGlade: LhystudiosDriver.<event_handler>
        self.context.plot_shift = self.checkbox_plot_shift.GetValue()
        try:
            _, driver, _ = self.context.root.device()
            driver.plot_planner.force_shift = self.context.plot_shift
        except (AttributeError, TypeError):
            pass

    def on_check_random_ppi(
        self, event=None
    ):  # wxGlade: LhystudiosDriver.<event_handler>
        self.context.random_ppi = self.checkbox_random_ppi.GetValue()

    def on_buffer_update(self, origin, value, *args):
        self.text_buffer_length.SetValue(str(value))

    def on_radio_interface(self, event):  # wxGlade: LhyConfigurationPanel.<event_handler>
        print("Event handler 'on_radio_interface' not implemented!")
        event.Skip()

    def spin_on_device_version(self, event):  # wxGlade: LhyConfigurationPanel.<event_handler>
        print("Event handler 'spin_on_device_version' not implemented!")
        event.Skip()

    def spin_on_device_index(self, event):  # wxGlade: LhyConfigurationPanel.<event_handler>
        print("Event handler 'spin_on_device_index' not implemented!")
        event.Skip()

    def spin_on_device_address(self, event):  # wxGlade: LhyConfigurationPanel.<event_handler>
        print("Event handler 'spin_on_device_address' not implemented!")
        event.Skip()

    def spin_on_device_bus(self, event):  # wxGlade: LhyConfigurationPanel.<event_handler>
        print("Event handler 'spin_on_device_bus' not implemented!")
        event.Skip()

    def on_text_address(self, event):  # wxGlade: LhyConfigurationPanel.<event_handler>
        print("Event handler 'on_text_address' not implemented!")
        event.Skip()

    def on_text_port(self, event):  # wxGlade: LhyConfigurationPanel.<event_handler>
        print("Event handler 'on_text_port' not implemented!")
        event.Skip()

    def on_check_rapid_between(self, event):  # wxGlade: LhyConfigurationPanel.<event_handler>
        print("Event handler 'on_check_rapid_between' not implemented!")
        event.Skip()

    def on_check_alt_raster(self, event):  # wxGlade: LhyConfigurationPanel.<event_handler>
        print("Event handler 'on_check_alt_raster' not implemented!")
        event.Skip()

    def on_check_twitchless(self, event):  # wxGlade: LhyConfigurationPanel.<event_handler>
        print("Event handler 'on_check_twitchless' not implemented!")
        event.Skip()

    def spin_on_bedwidth(self, event):  # wxGlade: LhyConfigurationPanel.<event_handler>
        print("Event handler 'spin_on_bedwidth' not implemented!")
        event.Skip()

    def spin_on_bedheight(self, event):  # wxGlade: LhyConfigurationPanel.<event_handler>
        print("Event handler 'spin_on_bedheight' not implemented!")
        event.Skip()

    def on_text_x_scale(self, event):  # wxGlade: LhyConfigurationPanel.<event_handler>
        print("Event handler 'on_text_x_scale' not implemented!")
        event.Skip()

    def on_text_y_scale(self, event):  # wxGlade: LhyConfigurationPanel.<event_handler>
        print("Event handler 'on_text_y_scale' not implemented!")
        event.Skip()


class LhystudiosDriverGui(MWindow):
    def __init__(self, *args, **kwds):
        super().__init__(692, 546, *args, **kwds)

        self.panel = LhystudiosConfigurationPanel(self, wx.ID_ANY, context=self.context)
        self.add_module_delegate(self.panel)
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(icons8_administrative_tools_50.GetBitmap())
        self.SetIcon(_icon)
        self.SetTitle(_("Lhystudios-Configuration"))

    def window_open(self):
        self.panel.pane_show()

    def window_close(self):
        self.panel.pane_hide()

    def window_preserve(self):
        return False

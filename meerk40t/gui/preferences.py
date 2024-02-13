#
# generated by wxGlade 0.9.3 on Thu Jun 27 21:45:40 2019
#
import platform

import wx

from meerk40t.kernel.kernel import signal_listener

from .choicepropertypanel import ChoicePropertyPanel
from .icons import icons8_administrative_tools
from .mwindow import MWindow
from .wxmribbon import RibbonEditor
from .wxutils import StaticBoxSizer, TextCtrl, wxButton

_ = wx.GetTranslation


class PreferencesUnitsPanel(wx.Panel):
    def __init__(self, *args, context=None, **kwds):
        # begin wxGlade: PreferencesUnitsPanel.__init__
        kwds["style"] = kwds.get("style", 0)
        wx.Panel.__init__(self, *args, **kwds)
        self.context = context

        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)

        self.radio_units = wx.RadioBox(
            self,
            wx.ID_ANY,
            _("Units"),
            choices=["mm", "cm", "inch", "mils"],
            majorDimension=1,
            style=wx.RA_SPECIFY_ROWS,
        )
        self.radio_units.SetToolTip(_("Set default units for guides"))
        sizer_1.Add(self.radio_units, 0, wx.EXPAND, 0)

        self.SetSizer(sizer_1)

        self.Layout()

        self.Bind(wx.EVT_RADIOBOX, self.on_radio_units, self.radio_units)

        self.radio_units.SetSelection(self._get_units_index())

    def on_radio_units(self, event):
        if event.Int == 0:
            self.set_mm()
        elif event.Int == 1:
            self.set_cm()
        elif event.Int == 2:
            self.set_inch()
        elif event.Int == 3:
            self.set_mil()

    def _get_units_index(self):
        p = self.context.root
        units = p.units_name
        if units == "mm":
            return 0
        if units == "cm":
            return 1
        if units in ("in", "inch", "inches"):
            return 2
        if units == "mil":
            return 3
        return 0

    def set_inch(self):
        p = self.context.root
        p.units_name = "inch"
        p.signal("units", p.units_name)

    def set_mil(self):
        p = self.context.root
        p.units_name = "mil"
        p.signal("units", p.units_name)

    def set_cm(self):
        p = self.context.root
        p.units_name = "cm"
        p.signal("units", p.units_name)

    def set_mm(self):
        p = self.context.root
        p.units_name = "mm"
        p.signal("units", p.units_name)


# end of class PreferencesUnitsPanel


class PreferencesLanguagePanel(wx.Panel):
    def __init__(self, *args, context=None, **kwds):
        # begin wxGlade: PreferencesLanguagePanel.__init__
        kwds["style"] = kwds.get("style", 0)
        wx.Panel.__init__(self, *args, **kwds)
        self.context = context

        sizer_2 = StaticBoxSizer(self, wx.ID_ANY, _("Language"), wx.HORIZONTAL)
        from .wxmeerk40t import supported_languages

        choices = [
            language_name
            for language_code, language_name, language_index in supported_languages
        ]
        self.combo_language = wx.ComboBox(
            self, wx.ID_ANY, choices=choices, style=wx.CB_READONLY
        )
        self.combo_language.SetToolTip(
            _("Select the desired language to use (requires a restart to take effect).")
        )
        sizer_2.Add(self.combo_language, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.SetSizer(sizer_2)

        self.Layout()

        self.context.setting(int, "language", 0)

        self.Bind(wx.EVT_COMBOBOX, self.on_combo_language, self.combo_language)
        # end wxGlade
        self.combo_language.SetSelection(self.context.language)

    def on_combo_language(self, event=None):
        lang = self.combo_language.GetSelection()
        if lang != -1 and self.context.app is not None:
            self.context.app.update_language(lang)
            self.context.signal("restart")


# end of class PreferencesLanguagePanel


class PreferencesSavingPanel(wx.Panel):
    def __init__(self, *args, context=None, **kwds):
        # begin wxGlade: PreferencesLanguagePanel.__init__
        kwds["style"] = kwds.get("style", 0)
        wx.Panel.__init__(self, *args, **kwds)
        self.context = context

        main_sizer = StaticBoxSizer(self, wx.ID_ANY, _("Management"), wx.HORIZONTAL)
        self.button_save = wxButton(self, wx.ID_ANY, _("Save"))
        self.button_save.SetToolTip(_("Immediately save the settings to disk"))
        self.button_export = wxButton(self, wx.ID_ANY, _("Export"))
        self.button_export.SetToolTip(
            _("Export the current settings to a different location")
        )
        self.button_import = wxButton(self, wx.ID_ANY, _("Import"))
        self.button_import.SetToolTip(_("Import a previously saved setting file"))
        main_sizer.Add(self.button_save, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.Bind(wx.EVT_BUTTON, self.on_button_save, self.button_save)
        main_sizer.AddStretchSpacer(1)
        main_sizer.Add(self.button_export, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        main_sizer.Add(self.button_import, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.SetSizer(main_sizer)
        self.Layout()
        self.Bind(wx.EVT_BUTTON, self.on_button_save, self.button_save)
        self.Bind(wx.EVT_BUTTON, self.on_button_import, self.button_import)
        self.Bind(wx.EVT_BUTTON, self.on_button_export, self.button_export)

    def on_button_save(self, event=None):
        self.context("flush\n")

    def on_button_export(self, event=None):
        dlg = wx.DirDialog(
            self,
            _("Choose target directory:"),
            style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST,
        )

        if dlg.ShowModal() == wx.ID_OK:
            self.context(f"setting_export {dlg.GetPath()}\n")
            wx.MessageBox(_("Export completed"), _("Info"), wx.OK | wx.ICON_INFORMATION)

        dlg.Destroy()

    def on_button_import(self, event=None):
        message = _("This will import a previously saved configuration file!") + "\n"
        message += (
            _(
                "This may make MeerK40t unworkable if the file does not have the right format!"
            )
            + "\n"
        )
        message += _("You do this at you own risk - are you really sure?")
        caption = _("Warning")
        dlg = wx.MessageDialog(
            self,
            message,
            caption,
            wx.YES_NO | wx.ICON_WARNING,
        )
        dlgresult = dlg.ShowModal()
        dlg.Destroy()
        if dlgresult != wx.ID_YES:
            return
        dlg = wx.FileDialog(
            self,
            message=_("Choose a previously saved configuration-file"),
            wildcard="Meerk40t-Config-Files (*.cfg)|*.cfg|All files (*.*)|*.*",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_PREVIEW,
        )
        dlgresult = dlg.ShowModal()
        if dlgresult == wx.ID_YES:
            myfile = dlg.GetPath()
            dlg.Destroy()
        else:
            dlg.Destroy()
            return

        self.context(f"setting_import {myfile}\n")
        wx.MessageBox(_("Import completed"), _("Info"), wx.OK | wx.ICON_INFORMATION)


class PreferencesPixelsPerInchPanel(wx.Panel):
    def __init__(self, *args, context=None, **kwds):
        # begin wxGlade: PreferencesPixelsPerInchPanel.__init__
        kwds["style"] = kwds.get("style", 0)
        wx.Panel.__init__(self, *args, **kwds)
        self.context = context

        sizer_3 = StaticBoxSizer(
            self, wx.ID_ANY, _("SVG Pixel Per Inch"), wx.HORIZONTAL
        )

        self.combo_svg_ppi = wx.ComboBox(
            self,
            wx.ID_ANY,
            choices=[
                _("96 px/in Inkscape"),
                _("72 px/in Illustrator"),
                _("90 px/in Old Inkscape"),
                _("Custom"),
            ],
            style=wx.CB_READONLY,
        )
        self.combo_svg_ppi.SetToolTip(
            _("Select the Pixels Per Inch to use when loading an SVG file")
        )
        sizer_3.Add(self.combo_svg_ppi, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        sizer_3.Add((20, 20), 0, 0, 0)

        self.text_svg_ppi = TextCtrl(
            self, wx.ID_ANY, "", check="float", style=wx.TE_PROCESS_ENTER, limited=True
        )
        self.text_svg_ppi.SetToolTip(
            _("Custom Pixels Per Inch to use when loading an SVG file")
        )
        sizer_3.Add(self.text_svg_ppi, 1, wx.EXPAND, 0)

        self.SetSizer(sizer_3)

        self.Layout()

        self.Bind(wx.EVT_COMBOBOX, self.on_combo_svg_ppi, self.combo_svg_ppi)
        self.text_svg_ppi.SetActionRoutine(self.on_text_svg_ppi)
        # end wxGlade

        context.elements.setting(float, "svg_ppi", 96.0)
        self.text_svg_ppi.SetValue(str(context.elements.svg_ppi))
        self.on_text_svg_ppi()

    def on_combo_svg_ppi(self, event=None):
        elements = self.context.elements
        ppi = self.combo_svg_ppi.GetSelection()
        if ppi == 0:
            elements.svg_ppi = 96.0
        elif ppi == 1:
            elements.svg_ppi = 72.0
        elif ppi == 2:
            elements.svg_ppi = 90.0
        else:
            elements.svg_ppi = 96.0
        self.text_svg_ppi.SetValue(str(elements.svg_ppi))

    def on_text_svg_ppi(self):
        elements = self.context.elements
        try:
            svg_ppi = float(self.text_svg_ppi.GetValue())
        except ValueError:
            return
        if svg_ppi == 96:
            if self.combo_svg_ppi.GetSelection() != 0:
                self.combo_svg_ppi.SetSelection(0)
        elif svg_ppi == 72:
            if self.combo_svg_ppi.GetSelection() != 1:
                self.combo_svg_ppi.SetSelection(1)
        elif svg_ppi == 90:
            if self.combo_svg_ppi.GetSelection() != 2:
                self.combo_svg_ppi.SetSelection(2)
        else:
            if self.combo_svg_ppi.GetSelection() != 3:
                self.combo_svg_ppi.SetSelection(3)
        elements.svg_ppi = svg_ppi


# end of class PreferencesPixelsPerInchPanel


class PreferencesMain(wx.Panel):
    def __init__(self, *args, context=None, **kwds):
        # begin wxGlade: PreferencesMain.__init__
        kwds["style"] = kwds.get("style", 0)
        wx.Panel.__init__(self, *args, **kwds)
        self.context = None
        self.SetHelpText("preferences")
        sizer_main = wx.BoxSizer(wx.VERTICAL)

        self.panel_units = PreferencesUnitsPanel(self, wx.ID_ANY, context=context)
        sizer_main.Add(self.panel_units, 0, wx.EXPAND, 0)

        self.panel_language = PreferencesLanguagePanel(self, wx.ID_ANY, context=context)
        sizer_main.Add(self.panel_language, 0, wx.EXPAND, 0)

        self.panel_ppi = PreferencesPixelsPerInchPanel(self, wx.ID_ANY, context=context)
        sizer_main.Add(self.panel_ppi, 0, wx.EXPAND, 0)

        self.panel_pref1 = ChoicePropertyPanel(
            self,
            id=wx.ID_ANY,
            context=context,
            choices="preferences",
            constraint=("-Classification", "-Gui", "-Scene"),
        )
        sizer_main.Add(self.panel_pref1, 1, wx.EXPAND, 0)

        self.panel_management = PreferencesSavingPanel(self, wx.ID_ANY, context=context)
        sizer_main.Add(self.panel_management, 0, wx.EXPAND, 0)

        self.SetSizer(sizer_main)

        self.Layout()
        # end wxGlade

    def delegates(self):
        yield self.panel_ppi
        yield self.panel_language
        yield self.panel_units
        yield self.panel_pref1
        yield self.panel_management


# end of class PreferencesMain

#
# class PreferencesPanel(wx.Panel):
#     def __init__(self, *args, context=None, **kwds):
#         # begin wxGlade: PreferencesPanel.__init__
#         kwds["style"] = kwds.get("style", 0)
#         wx.Panel.__init__(self, *args, **kwds)
#         self.context = context
#
#         sizer_settings = wx.BoxSizer(wx.VERTICAL)
#
#         self.panel_main = PreferencesMain(self, wx.ID_ANY, context=context)
#         sizer_settings.Add(self.panel_main, 1, wx.EXPAND, 0)
#
#         self.SetSizer(sizer_settings)
#
#         self.Layout()
#         # end wxGlade
#
#     def delegates(self):
#         yield self.panel_main


class Preferences(MWindow):
    def __init__(self, *args, **kwds):
        super().__init__(
            525,
            750,
            *args,
            style=wx.CAPTION
            | wx.CLOSE_BOX
            | wx.FRAME_FLOAT_ON_PARENT
            | wx.TAB_TRAVERSAL
            | (wx.RESIZE_BORDER if platform.system() != "Darwin" else 0),
            **kwds,
        )
        self.notebook_main = wx.aui.AuiNotebook(
            self,
            -1,
            style=wx.aui.AUI_NB_TAB_EXTERNAL_MOVE
            | wx.aui.AUI_NB_SCROLL_BUTTONS
            | wx.aui.AUI_NB_TAB_SPLIT
            | wx.aui.AUI_NB_TAB_MOVE,
        )
        self.sizer.Add(self.notebook_main, 1, wx.EXPAND, 0)

        # self.panel_main = PreferencesPanel(self, wx.ID_ANY, context=self.context)
        self.panel_main = PreferencesMain(self, wx.ID_ANY, context=self.context)
        inject_choices = [
            {
                "attr": "preset_classify_automatic",
                "object": self,
                "default": False,
                "type": bool,
                "style": "button",
                "label": _("Automatic"),
                "tip": _("Set options for a good automatic experience"),
                "help": "classification",
                "page": "Classification",
                "section": "_AA_Presets",
                "subsection": "_0_",
            },
            {
                "attr": "preset_classify_manual",
                "object": self,
                "default": False,
                "type": bool,
                "style": "button",
                "label": _("Manual"),
                "tip": _("Set options for complete manual control"),
                "help": "classification",
                "page": "Classification",
                "section": "_AA_Presets",
                "subsection": "_0_",
            },
            {
                "attr": "dummy",
                "default": "dummy",
                "object": self,
                "type": str,
                "style": "info",
                "label": _(
                    "Classification is the (automatic) process of assigning an element to an operation."
                )
                + "\n"
                + _("That link between element and operation is called an assignment."),
                "help": "classification",
                "page": "Classification",
                # "section": "_000_Information",
            },
        ]
        self.presets = [
            # object, property, automatic, manual
            (self.context.elements, "operation_default_empty", False, True),
            (self.context.elements, "classify_reverse", False, False),
            (self.context.elements, "classify_new", True, False),
            (self.context.elements, "classify_fuzzy", True, True),
            (self.context.elements, "classify_fuzzydistance", 100, 100),
            (self.context.elements, "classify_black_as_raster", True, True),
            (self.context.elements, "classify_default", True, False),
            (self.context.elements, "classify_autogenerate", True, False),
            # (self.context.elements, "classify_auto_inherit", False, True),
            (self.context.elements, "classify_on_color", True, False),
            (self.context.elements, "classify_autogenerate_both", True, True),
        ]
        self.panel_classification = ChoicePropertyPanel(
            self,
            id=wx.ID_ANY,
            context=self.context,
            choices="preferences",
            constraint="Classification",
            injector=inject_choices,
        )
        self.panel_classification.SetupScrolling()

        self.panel_gui = ChoicePropertyPanel(
            self,
            id=wx.ID_ANY,
            context=self.context,
            choices="preferences",
            constraint="Gui",
        )
        self.panel_gui.SetupScrolling()

        self.panel_scene = ChoicePropertyPanel(
            self,
            id=wx.ID_ANY,
            context=self.context,
            choices="preferences",
            constraint="Scene",
        )
        self.panel_scene.SetupScrolling()

        main_scene = getattr(self.context.root, "mainscene", None)
        color_choices = []
        local_default_color = []
        for key, value in main_scene.colors.__dict__.items():
            if not key.startswith("_") and isinstance(value, str):
                local_default_color.append(key)
        local_default_color.sort()
        section = ""
        for key in local_default_color:
            # Try to make a sensible name out of it
            keyname = key.replace("_", " ")
            idx = 1  # Intentionally
            while idx < len(keyname):
                if keyname[idx] in "0123456789" and keyname[idx - 1] != " ":
                    keyname = keyname[:idx] + " " + keyname[idx:]
                idx += 1
            keyname = keyname[0].upper() + keyname[1:]
            words = keyname.split()
            possible_section = words[0]
            if possible_section[0:2] != section[0:2]:
                section = possible_section
            color_choices.append(
                {
                    "attr": f"color_{key}",
                    "object": main_scene.colors,
                    "default": main_scene.colors[key],
                    "type": str,
                    "style": "color",  # hexa representation
                    "label": keyname,
                    "section": section,
                    "signals": ("refresh_scene", "theme"),
                }
            )

        color_choices.append(
            {
                "attr": "color_reset",
                "object": self,
                "type": bool,
                "style": "button",
                "label": _("Reset Colors to Default"),
                "section": "_ZZ_",
            }
        )

        self.panel_color = ChoicePropertyPanel(
            self,
            id=wx.ID_ANY,
            context=self.context,
            choices=color_choices,
            entries_per_column=12,
        )
        self.panel_color.SetupScrolling()

        self.panel_ribbon = RibbonEditor(self, wx.ID_ANY, context=self.context)

        self.notebook_main.AddPage(self.panel_main, _("General"))
        self.notebook_main.AddPage(self.panel_classification, _("Classification"))
        self.notebook_main.AddPage(self.panel_gui, _("GUI"))
        self.notebook_main.AddPage(self.panel_scene, _("Scene"))
        self.notebook_main.AddPage(self.panel_color, _("Colors"))
        self.notebook_main.AddPage(self.panel_ribbon, _("Ribbon"))

        self.panels = [
            self.panel_main,
            self.panel_classification,
            self.panel_gui,
            self.panel_scene,
            self.panel_color,
            self.panel_ribbon,
        ]
        self.panel_ids = ["main", "classification", "gui", "scene", "color", "ribbon"]
        self.context.setting(bool, "developer_mode", False)
        if self.context.developer_mode:
            panel_space = ChoicePropertyPanel(
                self, wx.ID_ANY, context=self.context, choices="space"
            )
            self.notebook_main.AddPage(panel_space, _("Coordinate Space"))
            self.panels.append(panel_space)
            self.panel_ids.append("space")
        self.Layout()
        self.restore_aspect(honor_initial_values=True)

        _icon = wx.NullIcon
        _icon.CopyFromBitmap(icons8_administrative_tools.GetBitmap())
        self.SetIcon(_icon)
        self.SetTitle(_("Preferences"))

    @signal_listener("preferences")
    def on_pref_signal(self, origin, *args):
        if not args:
            return
        panel = args[0]
        if panel and panel in self.panel_ids:
            self.Show()
            self.notebook_main.SetSelection(self.panel_ids.index(panel))

    @property
    def color_reset(self):
        # Not relevant
        return False

    @color_reset.setter
    def color_reset(self, value):
        if value:
            # We are resetting all GUI.colors
            self.context("scene color unset\n")
            self.context.signal("theme", True)

    @property
    def preset_classify_manual(self):
        # Not relevant
        return False

    @preset_classify_manual.setter
    def preset_classify_manual(self, value):
        if value:
            # We are setting presets for a couple of parameters
            for preset in self.presets:
                setattr(preset[0], preset[1], preset[3])
                self.context.signal(preset[1], preset[3], preset[0])

    @property
    def preset_classify_automatic(self):
        # Not relevant
        return False

    @preset_classify_automatic.setter
    def preset_classify_automatic(self, value):
        if value:
            # We are setting presets for a couple of parameters
            for preset in self.presets:
                setattr(preset[0], preset[1], preset[2])
                self.context.signal(preset[1], preset[2], preset[0])

    def delegates(self):
        yield from self.panels

    @staticmethod
    def sub_register(kernel):
        import platform

        if platform.system() != "Darwin":
            kernel.register(
                "button/config/Preferences",
                {
                    "label": _("Preferences"),
                    "icon": icons8_administrative_tools,
                    "tip": _("Opens Preferences Window"),
                    "action": lambda v: kernel.console("window toggle Preferences\n"),
                },
            )

    def window_open(self):
        pass

    def window_close(self):
        pass

    @staticmethod
    def menu_label():
        return _("Pr&eferences...\tCtrl-,")

    @staticmethod
    def menu_tip():
        return _("Show/Hide the Preferences window")

    @staticmethod
    def menu_id():
        return wx.ID_PREFERENCES

    @staticmethod
    def submenu():
        # suppress in tool-menu
        return "", "Preferences", True

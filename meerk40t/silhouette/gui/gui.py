

def plugin(service, lifecycle):
    if lifecycle == "invalidate":
        return not service.has_feature("wx")
    if lifecycle == "service":
        return "provider/device/silhouette"
    if lifecycle == "assigned":
        service("window toggle Configuration\n")
    if lifecycle == "added":
        # Define GUI information here.
        from meerk40t.silhouette.gui.silhouetteconfig import SilhouetteConfig
        from meerk40t.gui.icons import icons8_computer_support, icons8_pause, icons8_emergency_stop_button

        # Supports the * button beside the laserpanel device choice
        service.register("window/Configuration", SilhouetteConfig)
        service.register("winpath/Configuration", service)

        _ = service._

        # These are the buttons that appear in the ribbonbar
        service.register(
            "button/device/Configuration",
            {
                "label": _("Config"),
                "icon": icons8_computer_support,
                "tip": _("Opens device-specific configuration window"),
                "help": "devicesilhouette",
                "action": lambda v: service("window toggle Configuration\n"),
            },
        )

        service.register(
            "button/control/Pause",
            {
                "label": _("Pause"),
                "icon": icons8_pause,
                "tip": _("Pause the laser"),
                "help": "devicesilhouette",
                "action": lambda v: service("pause\n"),
            },
        )

        service.register(
            "button/control/Stop",
            {
                "label": _("Stop"),
                "icon": icons8_emergency_stop_button,
                "tip": _("Emergency stop the laser"),
                "help": "devicesilhouette",
                "action": lambda v: service("estop\n"),
            },
        )

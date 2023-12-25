"""
Silhouette Device Plugin
"""

from meerk40t.silhouette.device import SilhouetteDevice


def plugin(kernel, lifecycle=None):
    if lifecycle == "plugins":
        from .gui import gui

        return [gui.plugin]

    if lifecycle == "register":
        kernel.register("provider/device/silhouette", SilhouetteDevice)
        _ = kernel.translation
        kernel.register(
            "dev_info/silhouette-device",
            {
                "provider": "provider/device/silhouette",
                "friendly_name": _("Silhouette Vinyl Cutter"),
                "extended_info": _(
                    "Silhouette brand vinyl cutters use a drag knife."
                ),
                "priority": 0,
                "family": _("Silhouette"),
                "family_priority": 9,
                "choices": [
                    {
                        "attr": "label",
                        "default": "Silhouette",
                    },
                ],
            },
        )
    if lifecycle == "preboot":
        suffix = "silhouette"
        for d in kernel.derivable(suffix):
            kernel.root(f"service device start -p {d} {suffix}\n")

"""

"""
from meerk40t.core.view import View

from meerk40t.kernel import Service

from ..core.spoolers import Spooler
from ..core.units import Length
from .driver import SilhouetteDriver


class SilhouetteDevice(Service):
    """
    Silhouette Device Service.
    """

    def __init__(self, kernel, path, *args, choices=None, **kwargs):
        Service.__init__(self, kernel, path)

        _ = self._
        choices = [
            {
                "attr": "label",
                "object": self,
                "default": "Silhouette",
                "type": str,
                "label": _("Label"),
                "tip": _("What is this device called."),
                "section": "_00_General",
                "signals": "device;renamed",
            },
            {
                "attr": "bedwidth",
                "object": self,
                "default": "12in",
                "type": Length,
                "label": _("Width"),
                "tip": _("Width of the cutting mat."),
                "section": "_10_Dimensions",
                "subsection": "Bed",
                "signals": "bedsize",
                "nonzero": True,
            },
            {
                "attr": "bedheight",
                "object": self,
                "default": "12in",
                "type": Length,
                "label": _("Height"),
                "tip": _("Height of the cutting mat."),
                "section": "_10_Dimensions",
                "subsection": "Bed",
                "signals": "bedsize",
                "nonzero": True,
            },
        ]
        self.register_choices("bed_dim", choices)

        choices = [
            {
                "attr": "interface",
                "object": self,
                "default": "USB",
                "style": "combosmall",
                "choices": ["USB", "mock"],
                "display": [_("USB"), _("mock")],
                "type": str,
                "label": _("Interface Type"),
                "tip": _("Select the interface type for the Silhouette device"),
                "section": "_20_Protocol",
                "signals": "update_interface",
            },
        ]
        self.register_choices("interface", choices)

        choices = [
            {
                "attr": "interpolate",
                "object": self,
                "default": 50,
                "type": int,
                "label": _("Curve Interpolation"),
                "section": "_5_Config",
                "tip": _("Distance of the curve interpolation in mils"),
            },
        ]
        self.register_choices("silhouette-adv", choices)

        self.view = View(self.bedwidth, self.bedheight, dpi=508.0)

        self.state = 0

        self.driver = SilhouetteDriver(self)
        self.add_service_delegate(self.driver)

        self.spooler = Spooler(self, driver=self.driver)
        self.add_service_delegate(self.spooler)

    @property
    def viewbuffer(self):
        return "No buffer."

    @property
    def current(self):
        """
        @return: the location in units for the current known position.
        """
        return self.view.iposition(self.driver.native_x, self.driver.native_y)

    @property
    def native(self):
        """
        @return: the location in device native units for the current known position.
        """
        return self.driver.native_x, self.driver.native_y

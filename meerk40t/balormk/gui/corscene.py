"""
The corfile widget is an immediate mode gui swap in for the regular scene. The intent is to allow the user to enter the
required values to generate a lmc corfile by entering the required distances and allowing the calculation of the
correction file.

The use of immediate mode gui system is to allow for in-place editing of the values with robust interactions between
the different widget elements. Such as the highlight and use of different text boxes, which deselects the other entries.
"""

import bisect
import time
from math import tau

import wx

from meerk40t.gui.laserrender import LaserRender
from meerk40t.gui.scene.sceneconst import (
    RESPONSE_CHAIN,
    HITCHAIN_HIT,
)
from meerk40t.gui.scene.widget import Widget
from meerk40t.gui import icons
from meerk40t.gui.icons import icons8_detective
from meerk40t.gui.scene.scenespacewidget import SceneSpaceWidget
from meerk40t.tools.geomstr import Geomstr
from meerk40t.tools.pmatrix import PMatrix


def cor_file_geometry(s=0x6666):
    path = Geomstr()
    m = 0x7FFF

    def c(x, y):
        return complex(m + (s * x), m + (s * y))

    # Center Lines.
    path.line(c(-1.019, 0), c(1.019, 0))
    path.line(c(0, -1.019), c(0, 1.019))

    # Line Marker
    path.line(c(0.1, 0.3), c(0.1, -0.1))

    # Outer Edge
    path.line(c(-1, -1), c(1, -1))
    path.line(c(1, -1), c(1, 1))
    path.line(c(1, 1), c(-1, 1))
    path.line(c(-1, 1), c(-1, -1))

    # Square Marker
    path.line(c(-0.95, 0.75), c(-0.75, 0.75))
    path.line(c(-0.75, 0.75), c(-0.75, 0.95))
    path.line(c(-0.75, 0.95), c(-0.95, 0.95))
    path.line(c(-0.95, 0.95), c(-0.95, 0.75))

    # Diamond Marker
    path.line(c(0.85, -0.95), c(0.95, -0.85))
    path.line(c(0.95, -0.85), c(0.85, -0.75))
    path.line(c(0.85, -0.75), c(0.75, -0.85))
    path.line(c(0.75, -0.85), c(0.85, -0.95))

    return path


def cor_file_line_associated(s=0x6666):
    path = Geomstr()
    m = 0x7FFF

    def c(x, y):
        return complex(m + (s * x), m + (s * y))

    path.line(c(-1, -1), c(0, -1), settings=0)
    path.line(c(0, -1), c(1, -1), settings=1)

    path.line(c(1, -1), c(1, 0), settings=2)
    path.line(c(1, 0), c(1, 1), settings=3)

    path.line(c(1, 1), c(0, 1), settings=4)
    path.line(c(0, 1), c(-1, 1), settings=5)

    path.line(c(-1, 1), c(-1, 0), settings=6)
    path.line(c(-1, 0), c(-1, -1), settings=7)

    path.line(c(-1.019, 0), c(0, 0), settings=8)
    path.line(c(0, 0), c(1.019, 0), settings=9)

    path.line(c(0, -1.019), c(0, 0), settings=10)
    path.line(c(0, 0), c(0, 1.019), settings=11)
    return path


def register_scene(service):
    _ = service.kernel.translation

    service.register(
        "button/control/cor_file",
        {
            "label": _("cor_file"),
            "icon": icons8_detective,
            "tip": _("Create CorFile"),
            "help": "devicebalor",
            "action": lambda v: service("widget_corfile\n"),
        },
    )

    @service.console_command(
        "widget_corfile",
        hidden=True,
        help=_("Show the corfile scene widget"),
    )
    def scene_corfile(**kwargs):
        scene = service.root.opened.get("Scene")

        scene.push_stack(SceneSpaceWidget(scene))
        corfile_widget = CorFileWidget(scene)
        scene.widget_root.scene_widget.add_widget(-1, corfile_widget)
        scene.widget_root.focus_viewport_scene((0, 0, 0xFFFF, 0xFFFF), scene.gui.Size)
        scene.request_refresh()


def determine_font_size(
    gc: wx.GraphicsContext, font: wx.Font, message: str, box_width, box_height
):
    test_height = float("inf")
    test_width = float("inf")
    text_size = box_height * 0.75 / 0.9
    while test_height > box_height or test_width > box_width:
        # If we do not fit in the box, decrease size
        text_size *= 0.9
        # Set font size.
        try:
            font.SetFractionalPointSize(text_size)
        except AttributeError:
            font.SetPointSize(int(text_size))
        gc.SetFont(font, wx.BLACK)
        # Measure again.
        test_width, test_height = gc.GetTextExtent(message)
    return text_size, test_width, test_height


class CorFileWidget(Widget):
    """
    Widget for cor file creation routine.
    """

    def __init__(self, scene):
        Widget.__init__(self, scene, all=True)
        self.name = "Corfile"
        self.render = LaserRender(scene.context)
        self.geometry = cor_file_geometry()
        self.assoc = cor_file_line_associated()

        self.outline_pen = wx.Pen()
        self.outline_pen.SetColour(wx.BLACK)
        self.outline_pen.SetWidth(4)

        self.highlight_pen = wx.Pen()
        self.highlight_pen.SetColour(wx.BLUE)
        self.highlight_pen.SetWidth(200)

        self.background_brush = wx.Brush()
        self.background_brush.SetColour(wx.WHITE)

        self.hot_text_brush = wx.Brush()
        self.hot_text_brush.SetColour(wx.Colour(0xFF, 0xFF, 0xAA))
        self.active_text_brush = wx.Brush()
        self.active_text_brush.SetColour(wx.Colour(0xAA, 0xFF, 0xFF))
        self.default_text_brush = wx.Brush()
        self.default_text_brush.SetColour(wx.WHITE)

        self.active_brush = wx.LIGHT_GREY_BRUSH

        self.hot_brush = wx.MEDIUM_GREY_BRUSH

        self.font_color = wx.Colour()
        self.font_color.SetRGBA(0xFF000000)
        self.font = wx.Font(wx.SWISS_FONT)

        self.mouse_location = None
        self.was_clicked = None
        self.typed = ""

        self.active = None
        self.hot = None

        self.cursor = -1
        self.is_opened = True
        dev = scene.context.device
        self.geometry_size = 0x6666
        self._geometry_size = self.geometry_size
        self.text_fields = (
            (21500, 5200, 5000, 1000, dev, "cf_1"),
            (45000, 5200, 5000, 1000, dev, "cf_2"),
            (60000, 20000, 5000, 1000, dev, "cf_3"),
            (60000, 45000, 5000, 1000, dev, "cf_4"),
            (45000, 60000, 5000, 1000, dev, "cf_5"),
            (20000, 60000, 5000, 1000, dev, "cf_6"),
            (5200, 45000, 5000, 1000, dev, "cf_7"),
            (5200, 20000, 5000, 1000, dev, "cf_8"),
            (20000, 32000, 5000, 1000, dev, "cf_9"),
            (45000, 32000, 5000, 1000, dev, "cf_10"),
            (32000, 20000, 5000, 1000, dev, "cf_11"),
            (32000, 45000, 5000, 1000, dev, "cf_12"),
            (0xFFFF - 5000, -2000, 5000, 1000, self, "geometry_size"),
        )

        self.button_fields = (
            (
                -3000,
                0,
                3000,
                3000,
                icons.icons8_delete.GetBitmap(use_theme=False),
                self.close,
            ),
            (
                -3000,
                3000,
                3000,
                3000,
                icons.icons8_rotate_left.GetBitmap(use_theme=False),
                self.rotate_left,
            ),
            (
                -3000,
                6000,
                3000,
                3000,
                icons.icons8_rotate_right.GetBitmap(use_theme=False),
                self.rotate_right,
            ),
            (
                -3000,
                9000,
                3000,
                3000,
                icons.icons8_flip_horizontal.GetBitmap(use_theme=False),
                self.hflip,
            ),
            (
                -3000,
                12000,
                3000,
                3000,
                icons.icons8_flip_vertical.GetBitmap(use_theme=False),
                self.vflip,
            ),
            (
                0xFFFF - 5000,
                -6000,
                3000,
                3000,
                icons.icons8_up.GetBitmap(use_theme=False),
                self.geometry_size_increase,
            ),
            (
                0xFFFF - 2000,
                -6000,
                3000,
                3000,
                icons.icons8_down.GetBitmap(use_theme=False),
                self.geometry_size_decrease,
            ),
            (
                0xFFFF,
                0,
                3000,
                3000,
                icons.icons8_save.GetBitmap(use_theme=False),
                self.corfile_save,
            ),
        )

        self.countdown = 0
        self.message = None
        self.token = None

        self.toast_brush = wx.Brush()
        self.toast_pen = wx.Pen()
        self.toast_font = wx.SWISS_FONT

        self.brush_color = wx.Colour()
        self.pen_color = wx.Colour()
        self.font_color = wx.Colour()

        self.toast_pen.SetWidth(10)

        self.toast_alpha = None
        self.set_toast_alpha(255)

        self.scene.animate(self)

    def set_toast_alpha(self, alpha):
        """
        We set the alpha for all the colors.

        @param alpha:
        @return:
        """
        if alpha != self.toast_alpha:
            self.toast_alpha = alpha
            self.brush_color.SetRGBA(0xFFFFFF | alpha << 24)
            self.pen_color.SetRGBA(0x70FF70 | alpha << 24)
            self.font_color.SetRGBA(0x000000 | alpha << 24)
            self.toast_brush.SetColour(self.brush_color)
            self.toast_pen.SetColour(self.pen_color)

    def _contains(self, location, x, y, width, height):
        if location is None:
            return False
        if location[0] < x:
            return False
        if location[1] < y:
            return False
        if location[0] > (x + width):
            return False
        if location[1] > (y + height):
            return False
        return True

    def hit(self):
        return HITCHAIN_HIT

    def tick(self):
        self.scene.request_refresh()
        return self.is_opened

    def tab_next(self):
        self.hot += 1
        self.hot %= 12

    def tab_prev(self):
        self.hot += 11
        self.hot %= 12

    def event(
        self,
        window_pos=None,
        space_pos=None,
        event_type=None,
        nearest_snap=None,
        **kwargs,
    ):
        """
        Capture and deal with the double click event.

        Doubleclick in the grid loads a menu to remove the background.
        """
        if event_type in ("hover", "move"):
            self.mouse_location = space_pos
        if event_type == "leftdown":
            self.was_clicked = True
            # self.message = "Testing Toast..."
            # self.countdown = 100
        if event_type == "key_up":
            key = kwargs.get("keycode")
            if key:
                self.typed += key
            else:
                modifier = kwargs.get("modifiers")
                if modifier == "right":
                    self.cursor += 1
                elif modifier == "left":
                    self.cursor -= 1
                elif modifier == "tab":
                    self.cursor = -1
                    self.tab_next()
                elif modifier == "shift+tab":
                    self.cursor = -1
                    self.tab_prev()
        return RESPONSE_CHAIN

    def close(self):
        self.scene.pop_stack()
        self.scene.request_refresh()
        self.is_opened = False

    def rotate_left(self):
        matrix = PMatrix.rotate(tau / 4, 0x7FFF, 0x7FFF)
        self.geometry.transform3x3(matrix)

    def rotate_right(self):
        matrix = PMatrix.rotate(-tau / 4, 0x7FFF, 0x7FFF)
        self.geometry.transform3x3(matrix)

    def hflip(self):
        matrix = PMatrix.scale(-1, 1, 0x7FFF, 0x7FFF)
        self.geometry.transform3x3(matrix)

    def vflip(self):
        matrix = PMatrix.scale(1, -1, 0x7FFF, 0x7FFF)
        self.geometry.transform3x3(matrix)

    def corfile_save(self):
        root = self.scene.context.root
        _ = self.scene.context.kernel.translation
        filetype = "*.cor"
        with wx.FileDialog(
            root.gui,
            _("Export Corfile") + ": Doesn't currently export",
            wildcard=filetype,
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
        ) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            if not pathname.lower().endswith(".cor"):
                pathname += ".cor"

        with open(pathname, "wb") as f:
            f.write(b"Testing...")

    def geometry_size_increase(self):
        self.geometry_size += 100

    def geometry_size_decrease(self):
        self.geometry_size -= 100

    def process_textboxes(self, gc: wx.GraphicsContext, was_hovered: bool, index: int):
        """
        Process textboxes founds in self.text_fields

        @param gc:
        @param was_hovered:
        @param index:
        @return:
        """
        if not self.text_fields:
            return was_hovered, index
        gc.SetBrush(self.background_brush)
        gc.SetPen(self.outline_pen)
        for textfield in self.text_fields:
            index += 1
            x, y, width, height, obj, attr = textfield

            # Set brush based on state.
            if self.hot == index:
                gc.SetBrush(self.hot_text_brush)
            elif self.active == index:
                gc.SetBrush(self.active_text_brush)
            else:
                gc.SetBrush(self.default_text_brush)

            # Draw text box.
            gc.DrawRectangle(x, y, width, height)

            # Get the text from obj.attr
            text = str(getattr(obj, attr))
            if text is None:
                text = ""

            # Set text size by textfield height.
            text_size = height * 3.0 / 4.0  # px to pt conversion
            try:
                self.font.SetFractionalPointSize(text_size)
            except AttributeError:
                self.font.SetPointSize(int(text_size))

            # Set the font.
            gc.SetFont(self.font, wx.BLACK)

            if self._contains(self.mouse_location, x, y, width, height):
                # Is this textfield found at the last mouse location.
                self.scene.cursor("text")
                was_hovered = True
                self.active = index
                if self.was_clicked:
                    # Are we processing a click?
                    c_pos = gc.GetPartialTextExtents(text)

                    # Bisect the cursor location.
                    self.cursor = bisect.bisect(c_pos, (self.mouse_location[0] - x))
                    self.hot = index
                    self.was_clicked = False
            if obj is None or not hasattr(obj, attr):
                continue

            if self.hot == index and int(time.time() * 2) % 2 == 0:
                # Are we drawing a hot text box?
                if self.typed:
                    # Were typed events processed?
                    for char in self.typed:
                        new_cursor = self.cursor
                        if char == "\x00":
                            # This is a end or a home button.
                            new_cursor = len(text)
                        elif char == "\x08":
                            # This is a backspace.
                            if self.cursor != 0:
                                text = text[: self.cursor - 1] + text[self.cursor :]
                                new_cursor -= 1
                        else:
                            # This is normal text.
                            text = text[: self.cursor] + char + text[self.cursor :]
                            new_cursor += 1

                        try:
                            # Set the obj.attr value as a float()
                            setattr(obj, attr, float(text))
                        except ValueError:
                            continue
                        # If we correctly set the value, update the cursor location.
                        self.cursor = new_cursor
                    # Unset the typed data.
                    self.typed = ""
                if self.cursor > len(text) or self.cursor == -1:
                    # If cursor is new, or beyond, place it at the end.
                    self.cursor = len(text)

                # Get the x-offsets of the individual letters.
                c_pos = gc.GetPartialTextExtents(text)
                c_pos.insert(0, 0)

                # Draw the cursor, located at the cursor_position.
                gc.SetBrush(wx.BLACK_BRUSH)
                try:
                    cursor_pos = c_pos[self.cursor]
                except IndexError:
                    cursor_pos = 0
                gc.DrawRectangle(x + cursor_pos, y, 40, height)

            # Draw the text inside the textbox.
            gc.DrawText(text, x, y)

        if not was_hovered:
            # If nothing was hovered, restore the cursor to the arrow-type.
            self.scene.cursor("arrow")
        return was_hovered, index

    def process_buttons(self, gc: wx.GraphicsContext, was_hovered: bool, index: int):
        """
        Draw buttons registered in `self.button_fields`

        @param gc:
        @param was_hovered:
        @param index:
        @return:
        """
        if not self.button_fields:
            return was_hovered, index
        gc.SetBrush(self.background_brush)
        gc.SetPen(self.outline_pen)
        for i, button in enumerate(self.button_fields):
            index += 1
            x, y, width, height, bmp, click = button
            if self.active == index:
                # If this is an active button, draw a white background.
                gc.SetBrush(self.background_brush)
                gc.DrawRectangle(x, y, width, height)

            # Draw Icon.
            gc.DrawBitmap(bmp, x, y, width, height)

            if self._contains(self.mouse_location, x, y, width, height):
                # If mouse contained this point, set this as active.
                self.active = index
                was_hovered = True
                if self.was_clicked:
                    # If we are processing a click value, call the `click()` function.
                    self.hot = index
                    self.was_clicked = False
                    click()
        return was_hovered, index

    def process_toast(self, gc: wx.GraphicsContext):
        if self.countdown <= 0:
            self.message = None
        if not self.message:
            return
        alpha = 255
        if self.countdown <= 20:
            alpha = int(self.countdown * 12.5)
        self.set_toast_alpha(alpha)
        self.countdown -= 1

        area_width, area_height = 0xFFFF, 0xFFFF
        left = area_width * 0.1
        top = area_height * 0.8
        right = area_width * 0.9
        bottom = area_height * 0.9
        w = right - left
        h = bottom - top
        text_size, test_width, test_height = determine_font_size(
            gc, self.toast_font, self.message, w, h
        )

        try:
            self.toast_font.SetFractionalPointSize(text_size)
        except AttributeError:
            self.toast_font.SetPointSize(int(text_size))
        gc.SetFont(self.toast_font, self.font_color)

        gc.SetPen(self.toast_pen)
        gc.SetBrush(self.toast_brush)
        gc.DrawRectangle(left, top, w, h)

        toast_x = left + (w - test_width) / 2.0
        toast_y = top + (h - test_height) / 2.0
        gc.DrawText(self.message, toast_x, toast_y)

    def process_draw(self, gc: wx.GraphicsContext):
        """
        Draws the background on the scene.
        """
        unit_width = 0xFFFF
        unit_height = 0xFFFF
        if self._geometry_size != self.geometry_size:
            # Update the geometry if the size has changed.
            self._geometry_size = self.geometry_size
            self.geometry = cor_file_geometry(self.geometry_size)
            self.assoc = cor_file_line_associated(self.geometry_size)
        # Draw the background.
        gc.SetBrush(wx.WHITE_BRUSH)
        gc.DrawRectangle(0, 0, unit_width, unit_height)

        # Draw the geometry
        gc.SetPen(wx.BLACK_PEN)
        wx_path_geom = self.render.make_geomstr(gc, self.geometry)
        gc.DrawPath(wx_path_geom)

        if self.hot is not None and 0 <= self.hot < 12:
            # If a text box is hot, we draw the assoc line.
            gc.SetPen(self.highlight_pen)
            wx_path_assoc = self.render.make_geomstr(gc, self.assoc, settings=self.hot)
            gc.DrawPath(wx_path_assoc)

        if self.mouse_location:
            # Draw rectangle around mouse location.
            gc.DrawRectangle(
                self.mouse_location[0] - 500, self.mouse_location[1] - 500, 1000, 1000
            )

        # Draw text boxes.
        was_hovered, index = self.process_textboxes(gc, False, -1)

        # Draw buttons.
        was_hovered, index = self.process_buttons(gc, was_hovered, index)

        if self.message:
            self.process_toast(gc)

        if not was_hovered:
            # Nothing was hovered, there is no active.
            self.active = None

        # If click wasn't processed, it clicked nothing.
        self.was_clicked = False

    def signal(self, signal, *args, **kwargs):
        """
        Signal commands which draw the background and updates the grid when needed to recalculate the lines
        """
        pass

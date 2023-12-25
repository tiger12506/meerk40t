"""
Silhouette Driver

Converts generic commands of LaserJob, et al. into Silhouette code

Author: Tiger12506
Heavily references: https://github.com/fablabnbg/inkscape-silhouette
"""
import time
from meerk40t.core.cutcode.gotocut import GotoCut
from meerk40t.core.cutcode.homecut import HomeCut
from meerk40t.core.cutcode.linecut import LineCut
from meerk40t.core.cutcode.quadcut import QuadCut
from meerk40t.core.cutcode.cubiccut import CubicCut
from meerk40t.core.cutcode.waitcut import WaitCut

from ..tools.geomstr import Geomstr

# End of Text - marks the end of a command
CMD_ETX = b'\x03'
# Esacpe - send the escape byte
CMD_ESC = b'\x1b'

### Escape Commands
# End of Transmission - also can init device
CMD_EOT = b'\x04'
# Enquire command - returns device status
CMD_ENQ = b'\x05'
# Negative Acknowledge - also returns device tool setup
CMD_NAK = b'\x15'


class SilhouetteDriver:
    def __init__(self, service, channel=None, *args, **kwargs):
        super().__init__()
        self.service = service
        self.name = str(self.service)
        self.state = 0
        self.paused = False

        self.native_x = 0
        self.native_y = 0

        self.toolholder = 0  # TODO: Make settable as a parameter of operations

        self.queue = []

        self.out_pipe = print
        self.in_pipe = input

    def __repr__(self):
        return f"SilhouetteDriver({self.name})"

    def __call__(self, e, real=False):
        if real: self.out_pipe(e)
        else: print(e)

    def initialize(self):
        self(CMD_ESC + CMD_EOT)

    def status(self):
        self(CMD_ESC + CMD_ENQ)

    def query_info(self):
        self(f"FG")

    def hold_work(self, priority):
        return False

    def job_start(self, job):
        pass

    def move_abs(self, x, y):
        self.native_x = x
        self.native_y = y
        self(f"M{x},{y}")

    def draw_abs(self, x, y):
        self(f"D{x},{y}")
        self.native_x = x
        self.native_y = y

    def move_rel(self, dx, dy):
        x = self.native_x + dx
        y = self.native_y + dy
        self.move_abs(x, y)

    def set_tool(self):
        self(f"J{self.toolholder}")

    def set_pressure(self, pressure):
        self(f"FX{pressure}, {self.toolholder}")

    def set_speed(self, speed):
        self(f"!{speed},{self.toolholder}")

    def set_depth(self, depth):
        self(f"TF{depth},{self.toolholder}")

    def plot(self, plot):
        self.queue.append(plot)

    def plot_start(self):
        for q in self.queue:
            while self.hold_work(0):
                if self.service.kernel.is_shutdown:
                    return
                time.sleep(0.05)
            if isinstance(q, LineCut):
                if (self.native_x, self.native_y) != q.start:
                    self.move_abs(*q.start)
                self.draw_abs(*q.end)
            elif isinstance(q, QuadCut):
                if (self.native_x, self.native_y) != q.start:
                    self.move_abs(*q.start)
                interp = self.service.interpolate
                g = Geomstr()
                g.quad(complex(*q.start), complex(*q.c()), complex(*q.end))
                for p in list(g.as_equal_interpolated_points(distance=interp))[1:]:
                    while self.paused:
                        time.sleep(0.05)
                    self.draw_abs(p.real, p.imag)
            elif isinstance(q, CubicCut):
                if (self.native_x, self.native_y) != q.start:
                    self.move_abs(*q.start)
                interp = self.service.interpolate
                g = Geomstr()
                g.cubic(
                    complex(*q.start),
                    complex(*q.c1()),
                    complex(*q.c2()),
                    complex(*q.end),
                )
                for p in list(g.as_equal_interpolated_points(distance=interp))[1:]:
                    while self.paused:
                        time.sleep(0.05)
                    self.draw_abs(p.real, p.imag)
            elif isinstance(q, HomeCut):
                self.home()
            elif isinstance(q, WaitCut):
                self.wait(q.dwell_time)
            elif isinstance(q, GotoCut):
                self.move_abs(*q.end)
        self.queue.clear()
        return False

    def job_finish(self, job):
        pass

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def home(self):
        self.move_abs(0, 0)
        self.native_x = 0
        self.native_y = 0

    def wait(self, dwell_time):
        time.sleep(dwell_time)

    def laser_on(self):
        pass

    def laser_off(self):
        pass

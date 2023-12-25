"""
Silhouette Driver

Converts generic commands of LaserJob, et al. into Silhouette code

Author: Tiger12506
Heavily references: https://github.com/fablabnbg/inkscape-silhouette
"""
import time
from ..core.units import UNITS_PER_INCH, UNITS_PER_MIL, UNITS_PER_MM
from meerk40t.core.cutcode.gotocut import GotoCut
from meerk40t.core.cutcode.homecut import HomeCut
from meerk40t.core.cutcode.linecut import LineCut
from meerk40t.core.cutcode.waitcut import WaitCut

CMD_EOT = b'\x04'
CMD_ENQ = b'\x05'
CMD_ETX = b'\x03'


class SilhouetteDriver:
    def __init__(self, service, channel=None, *args, **kwargs):
        super().__init__()
        self.service = service
        self.name = str(self.service)
        self.state = 0

        self.native_x = 0
        self.native_y = 0

        self.stepper_step_size = UNITS_PER_MM * 0.05  # Characteristic of Silhouette machines, step size is 0.05mm
        self.queue = []

        self.out_pipe = print
        self.in_pipe = input

    def __repr__(self):
        return f"SilhouetteDriver({self.name})"

    def __call__(self, e, real=False):
        if real: self.out_pipe(e)
        else: print(e)

    def initialize(self):
        self.send_escaped(CMD_EOT)

    def status(self):
        self(CMD_ENQ)

    def hold_work(self, priority):
        self(f"spooler check: {priority}")
        return False

    def job_start(self, job):
        self(f"job started {job}")

    def move_abs(self, x, y):
        self(f"M{x},{y}")

    def draw_abs(self, x, y):
        self(f"D{x},{y}")

    def move_rel(self, dx, dy):
        self(f"move_rel({dx}, {dy})")

    def plot(self, plot):
        self(f"plot({plot})")
        self.queue.append(plot)

    def plot_start(self):
        self("plot_start()")
        for q in self.queue:
            while self.hold_work(0):
                if self.service.kernel.is_shutdown:
                    return
                time.sleep(0.05)
            if isinstance(q, LineCut):
                self.move_abs(*q.start)
                self.draw_abs(*q.end)
            elif isinstance(q, HomeCut):
                self.home()
            elif isinstance(q, WaitCut):
                self.wait(q.dwell_time)
            elif isinstance(q, GotoCut):
                self.move_abs(*q.end)
        self.queue.clear()
        return False

    def job_finish(self, job):
        self(f"job finished {job}")

    def pause(self):
        self("Pause!")

    def resume(self):
        self("Resume!")

    def home(self):
        self("Home!")

    def wait(self, dwell_time):
        time.sleep(dwell_time)

    def laser_on(self):
        self("Cutter down!")

    def laser_off(self):
        self("Cutter up!")
from ..core.units import UNITS_PER_INCH, UNITS_PER_MIL, UNITS_PER_MM

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
        self(f"move_abs({x}, {y})")

    def move_rel(self, dx, dy):
        self(f"move_rel({dx}, {dy})")

    def plot(self, cutobject):
        self(f"plot send? {cutobject}")

    def plot_start(self):
        self("plot start!")

    def job_finish(self, job):
        self(f"job finished {job}")

    def pause(self):
        self("Pause!")

    def resume(self):
        self("Resume!")

    def home(self):
        self("Home!")

    def laser_on(self):
        self("Cutter down!")

    def laser_off(self):
        self("Cutter up!")
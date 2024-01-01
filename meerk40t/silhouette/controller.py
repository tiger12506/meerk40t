"""
Silhouette Controller

I have no idea what this does, but I'm gonna find out while I write it
"""
import threading

from meerk40t.kernel import signal_listener


class SilhouetteController:
    def __init__(self, context):
        self.service = context
        self.connection = None

#        self.update_connection()

        self._sending_thread = None
        self._recving_thread = None

        self._sending_queue = []
        self._sending_lock = threading.Lock()

        self._log = None
        self._watchers = []

    def __repr__(self):
        return "SilhouetteController()"
#        return f"SilhouetteController('{self.service.location()}')"

    @signal_listener("update_interface")
    def update_connection(self, origin=None, *args):
        if self.service.interface == "USB":
            pass
#            self.connection = USBConnection(self.service, self)
        else: #Mock
            pass
#            self.connection = MockConnection(self.service, self)

    def log(self, data, type):
        for w in self._watchers:
            w(data, type=type)

    def _channel_log(self, data, type=None):
        pass

    def add_watcher(self, watcher):
        self._watchers.append(watcher)

    def remove_watcher(self, watcher):
        self._watchers.remove(watcher)

    def open(self):
        if self.connection.connected:
            return
        self.connection.connect()
        if not self.connection.connected:
            self.log("Could not connect.", type="event")
            return
        self.log("Connecting to Silhouette...", type="event")

    def close(self):
        if not self.connection.connected:
            return
        self.connection.disconnect()
        self.log("Disconnecting from Silhouette...", type="event")

    def write(self, data):
        self.start()
        self.service.signal("silhouette;write", data)
        with self._sending_lock:
            self._sending_queue.append(data)

    def start(self):
        self.open()
        if self._channel_log not in self._watchers:
            self.add_watcher(self._channel_log)

        if self._sending_thread is None:
            self._sending_thread = True # Avoid race condition
            self._sending_thread = self.service.threaded(
                self._sending,
                thread_name=f"sender-{self.service.location()}",
                result=self.stop,
                daemon=True,
            )
        if self._recving_thread is None:
            self._recving_thread = True # Avoid race condition
            self._recving_thread = self.service.threaded(
                self._recving,
                thread_name=f"recver-{self.service.location()}",
                result=self._rstop,
                daemon=True,
            )

    def _rstop(self, *args):
        self._recving_thread = None

    def _send(self, line):
        self.connection.write(line)
        self.log(line, type="send")

    def _recv(self):
        while self.connection.connected:
            response = None
            while not response:
                try: response = self.connection.read()
                except (ConnectionAbortedError, AttributeError):
                    return
                if not response:
                    time.sleep(0.01)
            self.service.signal("silhouette;response", response)
            self.log(response, type="recv")
            if response == "ok":
                # FIXME
                pass

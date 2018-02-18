from threading import Thread, Event


class RepeatingThread(Thread):
    def __init__(self, event, timeout, func, arg):
        super(RepeatingThread, self).__init__()
        self._event = event
        self._timeout = timeout
        self._func = func
        self._arg = arg

    def run(self):
        while not self._event.wait(self._timeout):
            self._func(self._arg)

    def is_set(self):
        return not self._event.is_set()

    def stop(self):
        self._event.set()

def get_trigger():
    return Event()
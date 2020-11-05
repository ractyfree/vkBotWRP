import threading

import traceback

class WorkerThread(threading.Thread):
    def __init__(self, func, *args):
        threading.Thread.__init__(self, name='Parsing')
        self.func = func
        self.args = args
        self._running = True
        self.start()

    def run(self):
        try:
            return self.func(*self.args)
        except Exception as e:
            print(
                "".join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)))
            return

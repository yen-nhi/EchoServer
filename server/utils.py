from threading import Thread


class CustomThread(Thread):
    def __init__(self, target, args):
        Thread.__init__(self, target=target, args=args)
        self.return_value = None

    def run(self):
        if self._target:
            self.return_value = self._target(*self._args)

    def join(self):
        Thread.join(self)
        return self.return_value


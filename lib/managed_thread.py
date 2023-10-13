import threading


class ManagedThread(threading.Thread):
    def __init__(self, target, *args, **kwargs):
        super().__init__(target=target, args=args, kwargs=kwargs)
        self.start()

    def run(self):
        super().run()
        self.join()

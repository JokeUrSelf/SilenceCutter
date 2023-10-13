from lib.observer import Notifier
from lib.path import Path
from lib.pub_sub import Broker


class OutputPath(Path):
    def __init__(self, broker: Broker):
        super().__init__()
        self.broker = broker
        self.notifier = Notifier()
        self.on_change = self.notifier.add_listeners

    def set_full_path(self, path):
        super().set_full_path(path)
        self.broker.publish("output_path", path)
        self.notifier.notify_listeners(path)

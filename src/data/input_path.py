from lib.observer import Notifier
from lib.pub_sub import Broker
from lib.path import Path


class InputPathData(Path):
    def __init__(self, broker: Broker):
        super().__init__()
        self.broker = broker
        self.on_change = Notifier()

    def set_full_path(self, path: str):
        super().set_full_path(path)
        self.broker.publish("input_path", self)
        self.on_change.notify_listeners(self)

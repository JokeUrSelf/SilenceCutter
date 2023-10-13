from abc import abstractmethod
from typing import Callable, Any, Union


class Listener:
    def __init__(self, callback: Callable[[Any], None] = None):
        self.callback = callback

    @abstractmethod
    def update(self, data):
        self.callback(data)


class Notifier:
    def __init__(self):
        self._listeners = []

    def add_listener(self, listener: Union[Callable[[Any], None], Listener]):
        self._listeners.append(
            listener if isinstance(listener, Listener)
            else Listener(listener)
        )

    def add_listeners(self, *args):
        for x in args: self.add_listener(x)

    def remove_listener(self, listener: Listener):
        self._listeners.remove(listener)

    def notify_listeners(self, data=None):
        for listener in self._listeners:
            listener.update(data)


class ValueChangeNotifier(Notifier):

    def __init__(self, value):
        super().__init__()
        self._value = value

    @property
    def value(self):
        return self._value

    # Setter method decorated as a property setter
    @value.setter
    def value(self, value):
        self.notify_listeners(value)
        self._value = value

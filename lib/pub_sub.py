from abc import abstractmethod


class Broker:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, mark, subscriber):
        if mark not in self.subscribers:
            self.subscribers[mark] = []
        self.subscribers[mark].append(subscriber)

    def unsubscribe(self, mark, subscriber):
        if mark in self.subscribers and subscriber in self.subscribers[mark]:
            self.subscribers[mark].remove(subscriber)

    def publish(self, mark, message):
        if mark in self.subscribers:
            for subscriber in self.subscribers[mark]:
                subscriber.notify(mark, message)


class Subscriber:
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def notify(self, mark, message):
        print(f"{self.name} received message: {message}")

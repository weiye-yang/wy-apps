import requests

from settings import PUSHOVER_TOKEN, PUSHOVER_USER


class Notifier:
    _url = "https://api.pushover.net/1/messages.json"

    def __init__(self) -> None:
        pass


    def notify(self, msg: str) -> None:
        requests.post(Notifier._url, data={
            "token": PUSHOVER_TOKEN,
            "user": PUSHOVER_USER,
            "message": msg,
        })


if __name__ == "__main__":
    n = Notifier()
    n.notify("This is a test")

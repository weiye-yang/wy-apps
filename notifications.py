import requests

from settings import PUSHOVER_TOKEN, PUSHOVER_USER


def pushover_notify(msg: str) -> None:
    requests.post("https://api.pushover.net/1/messages.json", data={
        "token": PUSHOVER_TOKEN,
        "user": PUSHOVER_USER,
        "message": msg,
    })


if __name__ == "__main__":
    pushover_notify("This is a test")

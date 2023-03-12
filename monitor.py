import argparse
import datetime as dt
import os
from time import sleep

from client import ON_TIME, OpenLDBWSClient, expected_time, minutes_diff
from get_departure_board import departure_board
from notifier import pushover_notify


def monitor(
        crs_from: str,
        crs_to: str,
        scheduled: str,
        repeat_seconds: int,
) -> None:
    client = OpenLDBWSClient()
    while True:
        res = client.get_departures(crs_from=crs_from, crs_to=crs_to)
        generation_time: dt.datetime = res.generatedAt
        datetime_str = generation_time.strftime("%X")
        service = [d for d in res.trainServices.service if d.std == scheduled]

        print("")
        if len(service) == 0:
            print(f"[{datetime_str}] No service from {res.locationName} to {res.filterLocationName} scheduled at time {scheduled}")
            break

        print(f"[{datetime_str}] Status of {scheduled} service from {res.locationName} to {res.filterLocationName}:")
        departure = service[0]
        departure_time = expected_time(departure.std, departure.etd)
        print(f"Expected departure: {departure_time}")

        calling_points = departure.subsequentCallingPoints.callingPointList[0].callingPoint
        arrival = [a for a in calling_points if a.crs == crs_to][0]
        arrival_time = expected_time(arrival.st, arrival.et)
        print(f"Expected arrival: {arrival_time}")

        print(f"Journey duration: {minutes_diff(departure_time, arrival_time)} minutes")

        if departure.etd != ON_TIME:
            pushover_notify(f"{crs_from}->{crs_to} {scheduled} service delayed; expected {departure.etd}")

        print(f"Sleeping for {repeat_seconds} seconds...")
        sleep(repeat_seconds)


def main(crs_from: str, crs_to: str, repeat_seconds: int) -> None:
    if repeat_seconds < 0:
        raise ValueError(f"repeat_seconds is {repeat_seconds}, but should be non-negative")
    departure_board(crs_from=crs_from, crs_to=crs_to)
    print("")
    default_time = "10:21"
    scheduled = input(f"Enter scheduled time to monitor as hh:mm [default {default_time}]: ").strip()
    if not scheduled:
        scheduled = default_time
    monitor(crs_from=crs_from, crs_to=crs_to, scheduled=scheduled, repeat_seconds=repeat_seconds)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # http://www.railwaycodes.org.uk/crs/crs0.shtm
    parser.add_argument("--crs_from", default="MAI")
    parser.add_argument("--crs_to", default="PAD")
    parser.add_argument("--repeat_seconds", type=int, default=0)
    args = parser.parse_args()
    main(crs_from=args.crs_from, crs_to=args.crs_to, repeat_seconds=args.repeat_seconds)
    os.system("pause")

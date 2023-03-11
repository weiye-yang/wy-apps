import argparse
import datetime as dt
import os

from client import OpenLDBWSClient, expected_time, minutes_diff
from get_departure_board import departure_board


def monitor(crs_from: str, crs_to: str, scheduled: str) -> None:
    client = OpenLDBWSClient()

    while True:
        res = client.get_departures(crs_from=crs_from, crs_to=crs_to)
        generation_time: dt.datetime = res.generatedAt
        datetime_str = generation_time.strftime("%X")
        service = [d for d in res.trainServices.service if d.std == scheduled]

        print("")
        if len(service) == 0:
            print(f"[{datetime_str}] No {scheduled} service from {res.locationName} to {res.filterLocationName} found")
            break

        print(f"[{datetime_str}] Details of {scheduled} service from {res.locationName} to {res.filterLocationName}:")
        departure = service[0]
        departure_time = expected_time(departure.std, departure.etd)
        calling_points = departure.subsequentCallingPoints.callingPointList[0].callingPoint
        arrival = [a for a in calling_points if a.crs == crs_to][0]
        arrival_time = expected_time(arrival.st, arrival.et)
        duration = minutes_diff(departure_time, arrival_time)
        print(f"{departure.etd}. Journey duration {duration} mins")


def main(crs_from: str, crs_to: str) -> None:
    departure_board(crs_from=crs_from, crs_to=crs_to)
    print("")
    default_time = "10:21"
    scheduled = input(f"Enter scheduled service to monitor as hh:mm [default {default_time}]:").strip()
    if not scheduled:
        scheduled = default_time
    monitor(crs_from=crs_from, crs_to=crs_to, scheduled=scheduled)
    os.system("pause")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # http://www.railwaycodes.org.uk/crs/crs0.shtm
    parser.add_argument("--fr", default="MAI")
    parser.add_argument("--to", default="PAD")
    args = parser.parse_args()
    main(crs_from=args.fr, crs_to=args.to)

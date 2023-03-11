import argparse
import datetime as dt
from time import sleep
from typing import List

from client import OpenLDBWSClient, minutes_diff, expected_time, parse_time


def monitor(crs_from: str, crs_to: str, scheduled: str) -> None:
    scheduled_time = parse_time(scheduled)  # Check it's a valid time
    client = OpenLDBWSClient()

    while True:
        res = client.get_departures(crs_from=crs_from, crs_to=crs_to)
        generation_time: dt.datetime = res.generatedAt
        datetime_str = generation_time.strftime("%X")

        service = [d for d in res.trainServices.service if d.std == scheduled]
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
        print(f"{departure.etd}. Duration {duration} mins")
    input("Press Enter to exit...")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # http://www.railwaycodes.org.uk/crs/crs0.shtm
    parser.add_argument("--fr", default="MAI")
    parser.add_argument("--to", default="PAD")
    parser.add_argument("--time", default="14:37")
    args = parser.parse_args()
    monitor(crs_from=args.fr, crs_to=args.to, scheduled=args.time)

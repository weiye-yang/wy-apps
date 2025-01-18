import argparse
import datetime as dt
from typing import Any, List, Tuple

from open_ldbws.client import OpenLDBWSClient, expected_time, minutes_diff


def departure_board(crs_from: str, crs_to: str) -> List[Tuple[Any, float]]:
    """
    Prints out a departure board
    :param crs_from: CRS of originating station
    :param crs_to: CRS of end station
    :return: List of pairs of (departure info, duration)
    """

    client = OpenLDBWSClient()
    res = client.get_departures(crs_from=crs_from, crs_to=crs_to)
    generation_time: dt.datetime = res.generatedAt
    datetime_str = generation_time.strftime("%X")
    print(f"[{datetime_str}] Direct trains from {res.locationName} to {res.filterLocationName}:")

    board = []
    for departure in res.trainServices.service:
        calling_points = departure.subsequentCallingPoints.callingPointList[0].callingPoint
        arrival = [a for a in calling_points if a.crs == crs_to][0]

        departure_time = expected_time(departure.std, departure.etd)
        expected_str = f"Expected {departure_time}" if departure_time != departure.std else "On time       "

        arrival_time = expected_time(arrival.st, arrival.et)
        duration = minutes_diff(departure_time, arrival_time)
        print(f"Scheduled {departure.std} - {expected_str}; Arriving {arrival_time}; Duration {duration} mins")

        effective_duration: float = float("inf") if duration is None else duration
        board.append((departure, effective_duration))
    return board


def main(crs_from: str, crs_to: str) -> None:
    departure_board(crs_from=crs_from, crs_to=crs_to)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # http://www.railwaycodes.org.uk/crs/crs0.shtm
    parser.add_argument("--fr", default="MAI")
    parser.add_argument("--to", default="PAD")
    args = parser.parse_args()
    main(crs_from=args.fr, crs_to=args.to)

import argparse
from client import OpenLDBWSClient


def departure_board(crs_from, crs_to):
    client = OpenLDBWSClient()
    res = client.get_departures(crs_from=crs_from, crs_to=crs_to)
    services = res.trainServices.service

    print(f"Direct trains from {res.locationName} to {res.filterLocationName}:")
    for departure in services:
        calling_points = departure.subsequentCallingPoints.callingPointList[0].callingPoint
        arrival = [a for a in calling_points if a.crs == crs_to][0]
        print(f"Departing {departure.std} - {departure.etd}, arriving {arrival.st} - {arrival.et}")
    input("Press Enter to exit...")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # http://www.railwaycodes.org.uk/crs/crs0.shtm
    parser.add_argument("--fr", default="MAI")
    parser.add_argument("--to", default="PAD")
    args = parser.parse_args()
    departure_board(crs_from=args.fr, crs_to=args.to)

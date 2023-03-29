import datetime as dt
from time import sleep
from typing import Callable, Optional

from zeep import Client, Settings, xsd
from zeep.plugins import HistoryPlugin

from settings import API_TOKEN

ON_TIME = "On time"


class OpenLDBWSClient:
    # One-line .txt containing token for the API. Let's not include it in the repo
    _request_delay = 5  # seconds - prevent us from hammering the API by accident

    def __init__(self) -> None:
        header = xsd.Element(
            "{http://thalesgroup.com/RTTI/2013-11-28/Token/types}AccessToken",
            xsd.ComplexType([
                xsd.Element(
                    "{http://thalesgroup.com/RTTI/2013-11-28/Token/types}TokenValue",
                    xsd.String()
                )
            ])
        )
        self._soap_headers = [header(TokenValue=API_TOKEN)]
        self._client = Client(
            wsdl="http://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2021-11-01",
            settings=Settings(strict=False),
            plugins=[HistoryPlugin()]
        )
        self._last_request = dt.datetime.min

    @staticmethod
    def _throttle_request(func) -> Callable:
        def throttled_func(self, *args, **kwargs):
            time_since_last = dt.datetime.now() - self._last_request
            if time_since_last.seconds < OpenLDBWSClient._request_delay:
                sleep_seconds = OpenLDBWSClient._request_delay
                print(f"Sleeping for {sleep_seconds} seconds to throttle requests...")
                sleep(sleep_seconds)
            res = func(self, *args, **kwargs)
            self._last_request = dt.datetime.now()
            return res
        return throttled_func

    @_throttle_request
    def get_departures(self, crs_from: str, crs_to: str):
        return self._client.service.GetDepBoardWithDetails(
            numRows=20,
            crs=crs_from,
            filterCrs=crs_to,
            _soapheaders=self._soap_headers
        )


def parse_time(hhmm: str) -> Optional[dt.time]:
    parts = hhmm.split(":")
    if len(parts) != 2:
        return None  # Cancelled/Delayed
    return dt.time(int(parts[0]), int(parts[1]))


def minutes_diff(before: str, after: str) -> Optional[int]:
    before_time = parse_time(before)
    if before_time is None:
        return None
    after_time = parse_time(after)
    if after_time is None:
        return None

    # Arbitrary date. But if after time is earlier, then assume it is the next day
    before_dt = dt.datetime.combine(dt.date(1, 1, 1), before_time)
    after_date = dt.date(1, 1, 2) if after_time < before_time else dt.date(1, 1, 1)
    after_dt = dt.datetime.combine(after_date, after_time)

    td = after_dt - before_dt
    return td.seconds // 60


def expected_time(st: str, et: str) -> str:
    return st if et == ON_TIME else et

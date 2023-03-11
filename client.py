import datetime as dt
from zeep import xsd, Client, Settings
from zeep.plugins import HistoryPlugin

# One-line .txt containing token for the API. Let's not include it in the repo
FILENAME = r"C:\Users\User\OneDrive\Documents\OpenLDBWS.txt"


class OpenLDBWSClient:
    def __init__(self) -> None:
        with open(FILENAME) as f:
            content = f.readlines()
        if len(content) != 1:
            raise ValueError(f"Expecting only one line in file '{FILENAME}'. Instead have {len(content)}")
        header = xsd.Element(
            "{http://thalesgroup.com/RTTI/2013-11-28/Token/types}AccessToken",
            xsd.ComplexType([
                xsd.Element(
                    "{http://thalesgroup.com/RTTI/2013-11-28/Token/types}TokenValue",
                    xsd.String()
                )
            ])
        )
        self._soap_headers = [header(TokenValue=content[0])]

        wsdl = "http://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2021-11-01"
        self._client = Client(wsdl=wsdl, settings=Settings(strict=False), plugins=[HistoryPlugin()])

    def get_departures(self, crs_from: str, crs_to: str):
        return self._client.service.GetDepBoardWithDetails(
            numRows=20,
            crs=crs_from,
            filterCrs=crs_to,
            _soapheaders=self._soap_headers
        )


def parse_time(hhmm: str) -> dt.time:
    parts = hhmm.split(":")
    if len(parts) != 2:
        raise ValueError(f"Cannot parse time {hhmm}")
    return dt.time(int(parts[0]), int(parts[1]))


def minutes_diff(before: str, after: str) -> int:
    before_time = parse_time(before)
    after_time = parse_time(after)

    # Arbitrary date. But if after time is earlier, then assume it is the next day
    before_dt = dt.datetime.combine(dt.date(1, 1, 1), before_time)
    after_date = dt.date(1, 1, 2) if after_time < before_time else dt.date(1, 1, 1)
    after_dt = dt.datetime.combine(after_date, after_time)

    td = after_dt - before_dt
    return td.seconds // 60


def expected_time(st: str, et: str) -> str:
    return st if et == "On time" else et

from zeep import xsd, Client, Settings
from zeep.plugins import HistoryPlugin

# One-line .txt containing token for the API. Let's not include it in the repo
FILENAME = r"C:\Users\User\OneDrive\Documents\OpenLDBWS.txt"


class OpenLDBWSClient:
    def __init__(self):
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

    def get_departures(self, crs_from, crs_to):
        return self._client.service.GetDepBoardWithDetails(
            numRows=20,
            crs=crs_from,
            filterCrs=crs_to,
            _soapheaders=self._soap_headers
        )

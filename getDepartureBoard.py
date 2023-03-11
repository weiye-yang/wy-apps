#
# Open Live Departure Boards Web Service (OpenLDBWS) API Demonstrator
# Copyright (C)2018 OpenTrainTimes Ltd.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from zeep import Client, Settings, xsd
from zeep.plugins import HistoryPlugin


class OpenLDBWSClient:
    def __init__(self):
        # Let's not include my token in the repo
        filename = r"C:\Users\User\OneDrive\Documents\OpenLDBWS.txt"
        with open(filename) as f:
            content = f.readlines()
        if len(content) != 1:
            raise ValueError(f"Expecting only one line in file '{filename}'. Instead have {len(content)}")
        header = xsd.Element(
            "{http://thalesgroup.com/RTTI/2013-11-28/Token/types}AccessToken",
            xsd.ComplexType([
                xsd.Element(
                    "{http://thalesgroup.com/RTTI/2013-11-28/Token/types}TokenValue",
                    xsd.String()),
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


def main(crs_from, crs_to):
    client = OpenLDBWSClient()
    res = client.get_departures(crs_from=crs_from, crs_to=crs_to)
    services = res.trainServices.service

    print(f"Direct trains from {res.locationName} to {res.filterLocationName}:")
    for departure in services:
        calling_points = departure.subsequentCallingPoints.callingPointList[0].callingPoint
        arrival = [a for a in calling_points if a.crs == to][0]
        print(f"Departing {departure.std} - {departure.etd}, arriving {arrival.st} - {arrival.et}")


if __name__ == "__main__":
    # http://www.railwaycodes.org.uk/crs/crs0.shtm
    fr = "MAI"
    to = "PAD"
    # fr, to = to, fr
    main(crs_from=fr, crs_to=to)

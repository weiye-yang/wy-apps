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


def main(crs_from, crs_to):

    # Let's not include my token in the repo
    filename = r"C:\Users\User\OneDrive\Documents\OpenLDBWS.txt"
    with open(filename) as f:
        content = f.readlines()
    if len(content) != 1:
        raise ValueError(f"Expecting only one line in file '{filename}'. Instead have {len(content)}")

    wsdl = "http://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2021-11-01"
    client = Client(wsdl=wsdl, settings=Settings(strict=False), plugins=[HistoryPlugin()])

    header = xsd.Element(
        "{http://thalesgroup.com/RTTI/2013-11-28/Token/types}AccessToken",
        xsd.ComplexType([
            xsd.Element(
                "{http://thalesgroup.com/RTTI/2013-11-28/Token/types}TokenValue",
                xsd.String()),
        ])
    )

    res = client.service.GetDepBoardWithDetails(
        numRows=10,
        crs=crs_from,
        filterCrs=crs_to,
        _soapheaders=[header(TokenValue=content[0])]
    )
    services = res.trainServices.service

    print("Trains at " + res.locationName)
    print("===============================================================================")
    for t in services:
        print(t.std + " to " + t.destination.location[0].locationName + " - " + t.etd)


if __name__ == "__main__":
    # http://www.railwaycodes.org.uk/crs/crs0.shtm
    fr = "PAD"
    to = "MAI"
    # fr, to = to, fr
    main(crs_from=fr, crs_to=to)

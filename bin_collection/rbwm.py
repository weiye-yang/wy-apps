import argparse
import datetime as dt
from collections import defaultdict

import dateparser
import requests
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta

from settings import URPN


def main(urpn: str) -> None:
    url = "https://forms.rbwm.gov.uk/bincollections?uprn=" + urpn
    content = requests.get(url).text
    soup = BeautifulSoup(content, features="html.parser")
    next_collection_div = soup.find("div", {"class": "widget-bin-collections"})
    body = next_collection_div.find("tbody")

    results = defaultdict(set)
    for tr in body.find_all("tr"):
        row = [tag.get_text() for tag in tr.find_all("td")]
        if len(row) != 2:
            raise ValueError(f"Unexpected <tr> {row}")
        row_date = dateparser.parse(row[1]).date()
        results[row_date].add(row[0])

    tomorrow = dt.date.today() + relativedelta(days=1)
    tomorrow_bins = results.get(tomorrow)
    if tomorrow_bins is None:
        print(f"No bins collected tomorrow {tomorrow}")
    else:
        print(f"Bins collected tomorrow {tomorrow}: {tomorrow_bins}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--urpn", default=URPN)
    args = parser.parse_args()
    main(args.urpn)
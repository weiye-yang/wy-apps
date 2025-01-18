import argparse
import datetime as dt
from collections import defaultdict

import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

from notifications import pushover_notify
from settings import URPN_DEFAULT


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
        row_date = parse(row[1]).date()
        results[row_date].add(row[0])

    tomorrow = dt.date.today() + relativedelta(days=1)
    bins = results.get(tomorrow, set())
    num_bins = len(bins)
    if num_bins == 0:
        message = f"No bin collection on {tomorrow}"
    else:
        bins_str = ", ".join(sorted(bins))
        message = f"{num_bins} bin collection(s) on {tomorrow}: {bins_str}"
        pushover_notify(message)
    print(message)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--urpn", default=URPN_DEFAULT)
    args = parser.parse_args()
    main(args.urpn)
import argparse
import datetime as dt
from collections import defaultdict

import requests
from bs4 import BeautifulSoup, Tag
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

from notifications import pushover_notify
from settings import URPN_DEFAULT


class CollectionType(str):
    pass

def bin_collection_table(urpn: str) -> dict[dt.date, set[CollectionType]]:
    url = "https://forms.rbwm.gov.uk/bincollections?uprn=" + urpn
    content = requests.get(url).text
    soup = BeautifulSoup(content, features="html.parser")
    next_collection_div = soup.find("div", {"class": "widget-bin-collections"})
    if not isinstance(next_collection_div, Tag):
        raise ValueError("Could not find Next Collection div")
    body = next_collection_div.find("tbody")
    if not isinstance(body, Tag):
        raise ValueError("Could not find collection body")
    results: dict[dt.date, set[CollectionType]] = defaultdict(set)
    for tr in body.find_all("tr"):
        if isinstance(tr, Tag):
            row = [tag.get_text() for tag in tr.find_all("td")]
            if len(row) != 2:
                raise ValueError(f"Unexpected <tr> {row}")
            row_date = parse(row[1]).date()
            results[row_date].add(CollectionType(row[0]))
    return results


def main(urpn: str) -> None:
    results = bin_collection_table(urpn)
    if not results:
        raise ValueError("No bin collection results found")

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
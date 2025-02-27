import requests
from bs4 import BeautifulSoup
from waste_collection_schedule import Collection  # type: ignore[attr-defined]
from waste_collection_schedule.service.ICS import ICS

TITLE = "Abfallwirtschaftsbetrieb Esslingen"
DESCRIPTION = "Source for AWB Esslingen, Germany"
URL = "https://www.awb-es.de"

TEST_CASES = {
    "Aichwald": {"city": "Aichwald", "street": "Alte Dorfstrasse"},
    "Kohlberg": {"city": "Kohlberg", "street": "alle Straßen"},
}

HEADERS = {"user-agent": "Mozilla/5.0 (xxxx Windows NT 10.0; Win64; x64)"}


class Source:
    def __init__(self, city, street=None):
        self._city = city
        self._street = street
        self._ics = ICS()

    def fetch(self):
        session = requests.Session()

        params = {
            "city": self._city,
            "street": self._street,
            "direct": "true",
        }
        r = session.get(
            "https://www.awb-es.de/abfuhr/abfuhrtermine/__Abfuhrtermine.html",
            params=params,
        )
        r.raise_for_status()

        soup = BeautifulSoup(r.text, features="html.parser")
        downloads = soup.find_all("a", href=True)
        ics_url = None
        for download in downloads:
            href = download.get("href")
            if "t=ics" in href:
                ics_url = href
                break

        if ics_url is None:
            raise Exception(f"ics url not found")

        # get ics file
        r = session.get(ics_url, headers=HEADERS)
        r.raise_for_status()

        # parse ics file
        dates = self._ics.convert(r.text)

        entries = []
        for d in dates:
            entries.append(Collection(d[0], d[1]))
        return entries

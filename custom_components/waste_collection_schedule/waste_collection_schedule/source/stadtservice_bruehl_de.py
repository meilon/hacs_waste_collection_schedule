import logging
import datetime
import requests
from bs4 import BeautifulSoup
from waste_collection_schedule import Collection
from waste_collection_schedule.service.ICS import ICS

TITLE = "StadtService Brühl"
DESCRIPTION = "Source für Abfallkalender StadtService Brühl"
URL = "https://services.stadtservice-bruehl.de/abfallkalender/"
TEST_CASES = {
  "TEST1" : {"strasse":"Badorfer Straße","hnr":"1" }
}

_LOGGER = logging.getLogger(__name__)

class Source:
    def __init__(self, strasse, hnr):
        self._strasse = strasse
        self._hnr = hnr
        self._ics = ICS()

    def fetch(self):

        today = datetime.date.today()
        year = today.year
        # Get District
        data = {
        'street': self._strasse,
        'street_number': self._hnr,
        'send_street_and_nummber_data': ''
        }

        r = requests.post('https://services.stadtservice-bruehl.de/abfallkalender/', data=data)

        if r.status_code != 200:
            _LOGGER.error("Error querying calender data")
            return []

        #print(r.text)
        soup = BeautifulSoup(r.text, "html.parser")

        for tag in soup.find_all("input", type="hidden"):
            #print(tag["name"])
            #print(tag["value"])
            if (tag["name"] == "post_district"): post_district = tag["value"]

        if post_district == '':
            _LOGGER.error("Unable to get district")
            return []

        #print(post_district);
        #Get ICAL
        data = {
          'post_year': year,
          'post_district': post_district,
          'post_street_name': self._strasse,
          'post_street_number': self._hnr,
          'checked_waste_type_hausmuell': 'on',
          'checked_waste_type_gelber_sack': 'on',
          'checked_waste_type_altpapier': 'on',
          'checked_waste_type_bio': 'on',
          'checked_waste_type_weihnachtsbaeume': 'on',
          'checked_waste_type_strassenlaub': 'on',
          'form_page_id': '9',
          'reminder_time': '8',
          'send_ics_download_configurator_data': ''
        }

        r = requests.post('https://services.stadtservice-bruehl.de/abfallkalender/individuellen-abfuhrkalender-herunterladen/', data=data)

        if r.status_code != 200:
            _LOGGER.error("Error querying calender data")
            return []

        print(r.text)
        dates = self._ics.convert(r.text)

        entries = []
        for d in dates:
            entries.append(Collection(d[0],d[1]))

        return entries

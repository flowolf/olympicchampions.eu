#!/usr/bin/env python

import os

from datetime import datetime

import requests


class Champions(object):

    FLAG_MAP = {
        "algeria": "dz",
        "argentina": "ar",
        "armenia": "am",
        "australia": "au",
        "austria": "at",
        "azerbaijan": "az",
        "bahamas": "bs",
        "bahrain": "bh",
        "belarus": "by",
        "belgium": "be",
        "brazil": "br",
        "canada": "ca",
        "china": "cn",
        "chinese-taipei": "zz",
        "colombia": "co",
        "croatia": "hr",
        "cuba": "cu",
        "czech-republic": "cz",
        "denmark": "dk",
        "egypt": "eg",
        "estonia": "ee",
        "ethiopia": "et",
        "fiji": "fj",
        "france": "fr",
        "georgia": "ge",
        "germany": "de",
        "great-britain": "gb",
        "greece": "gr",
        "grenada": "gd",
        "hungary": "hu",
        "independent-olympic-athletes": "_Olimpic_Movement",
        "indonesia": "id",
        "iran": "ir",
        "ireland": "ie",
        "israel": "il",
        "italy": "it",
        "jamaica": "jm",
        "japan": "jp",
        "kazakhstan": "kz",
        "kenya": "ke",
        "kosovo": "_Kosovo",
        "kyrgyzstan": "kg",
        "lithuania": "lt",
        "malaysia": "my",
        "moldova": "md",
        "mongolia": "mn",
        "morocco": "ma",
        "netherlands": "nl",
        "new-zealand": "nz",
        "north-korea": "kp",
        "norway": "no",
        "philippines": "ph",
        "poland": "po",
        "portugal": "pt",
        "puerto-rico": "pr",
        "qatar": "qa",
        "romania": "ro",
        "russia": "ru",
        "serbia": "rs",
        "singapore": "sg",
        "slovakia": "sk",
        "slovenia": "si",
        "south-africa": "za",
        "south-korea": "kr",
        "spain": "es",
        "sweden": "se",
        "switzerland": "ch",
        "thailand": "th",
        "tunisia": "tn",
        "turkey": "tr",
        "ukraine": "ua",
        "united-arab-emirates": "ae",
        "united-states": "us",
        "uzbekistan": "uz",
        "venezuela": "ve",
        "vietnam": "vn",
        "europe": "_European_Union"
    }

    EUROPE = (
        "austria",
        "belgium",
        "bulgaria",
        "croatia",
        "cyprus",
        "czech-republic",
        "denmark",
        "estonia",
        "finland",
        "france",
        "germany",
        "greece",
        "hungary",
        "ireland",
        "italy",
        "latvia",
        "lithuania",
        "luxembourg",
        "malta",
        "netherlands",
        "poland",
        "portugal",
        "romania",
        "slovakia",
        "slovenia",
        "spain",
        "sweden",
    )

    def __init__(self):
        path = os.path.dirname(__file__)
        self.template = os.path.join(path, "template.html")
        self.document = os.path.join(path, "index.html")

    def get_medals(self):

        medals = requests.get("http://www.medalbot.com/api/v1/medals").json()

        europe = {
            "bronze_count": 0,
            "country_name": "The European Union",
            "gold_count": 0,
            "id": "europe",
            "place": 0,
            "silver_count": 0,
            "total_count": 0
        }
        r = []
        for medal in medals:
            if medal["id"] in self.EUROPE:
                for attribute in ("bronze", "silver", "gold", "total"):
                    attribute += "_count"
                    europe[attribute] += medal[attribute]
                continue
            r.append(medal)
        r.append(europe)

        return r

    def get_flag(self, slug):
        return self.FLAG_MAP[slug]

    def get_table(self):

        sorted_medals = sorted(
            self.get_medals(), key=lambda __: __["total_count"])

        r = (
            '<table class="table table-responsive table-striped champions">'
                '<tr>'
                    '<th>Rank</th>'
                    '<th colspan="2">Nation</th>'
                    '<th class="hidden-xxs">Bronze</th>'
                    '<th class="hidden-xxs">Silver</th>'
                    '<th class="hidden-xxs">Gold</th>'
                    '<th>Total</th>'
                '</tr>'
        )
        row = (
            '<tr>'
                '<td class="rank">{}</td>'
                '<td class="f32"><span class="flag {}"></span></td>'
                '<td class="name">{}</td>'
                '<td class="bronze hidden-xxs">{}</td>'
                '<td class="silver hidden-xxs">{}</td>'
                '<td class="gold hidden-xxs">{}</td>'
                '<td class="total">{}</td>'
            '</tr>'
        )
        for i, medal in enumerate(list(reversed(sorted_medals))[:10]):
            r += row.format(
                i + 1,
                self.get_flag(medal["id"]),
                medal["country_name"],
                medal["bronze_count"],
                medal["silver_count"],
                medal["gold_count"],
                medal["total_count"]
            )

        return r + '</table>'

    def draw_document(self):
        with open(self.template) as template:
            with open(self.document, "w") as document:
                document.write(
                    template.read()
                        .replace("{{ table }}", self.get_table())
                        .replace("{{ time }}", datetime.utcnow().isoformat())
                )

if __name__ == "__main__":
    Champions().draw_document()

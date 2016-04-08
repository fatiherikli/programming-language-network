# -*- coding: utf-8 -*-
import json
import requests
from lxml import html

BASE_URL = "https://en.wikipedia.org"
LIST_URL = "%s/wiki/List_of_programming_languages" % BASE_URL

ATTRIBUTES = ["Influenced", "Influenced by", "OS", "License",
              "Paradigm(s)", "Appeared in", "Developer", "Designed by",
              "Website", "Dialects", "Major implementations",
              "Typing discipline", "Implementation language", "Developer"]

LINK_ATTRS = ["Website"]


def normalize_data(value):
    # remove citations
    value = ''.join([
        part.split('[')[0]
        for part in value.split(']')])
    value = value.replace("&quot;", "")

    # remove needless data
    value = value.replace('Multi-paradigm:', '')

    # strip white spaces
    value = value.strip()

    # remove relative years
    if 'years ago' in value:
        value = value.split(';')[0]

    return value


def normalize_conjunctions(value):
    return (value.replace(' and ', ', ')
                 .replace(' & ', ','))


def fetch_details(url):
    details = {}
    source = requests.get(url).content
    doc = html.fromstring(source)
    rows = doc.cssselect(".infobox tr")

    if not rows:
        return details

    for row in rows:
        try:
            header = row.cssselect("th")[0]
        except IndexError:
            continue

        attribute = header.text_content().strip()

        if not attribute in ATTRIBUTES:
            continue

        data = row.cssselect("td")[0]

        if attribute in LINK_ATTRS:
            details[attribute] = [link.attrib['href']
                                  for link in data.cssselect("a")]
            continue

        splitter = '\n' if not ',' in data.text_content() else ','

        content = normalize_conjunctions(data.text_content()).split(splitter)

        normalized = map(normalize_data, content)

        details[attribute] = normalized

    return details


def main():
    result = {}
    source = requests.get(LIST_URL).content
    doc = html.fromstring(source)
    for link in doc.cssselect("table.multicol td a"):
        try:
            details = fetch_details(BASE_URL + link.attrib['href'])
            result[link.text] = details
            print link.text
        except Exception as e:
            print e

    json.dump(result, open('../data/data.json', 'w'))


if __name__ == "__main__":
    main()

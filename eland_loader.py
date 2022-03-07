import csv
from connection import estf
from elasticsearch import helpers

with open('data.csv', encoding='utf8') as f:
    reader = csv.DictReader(f)
    helpers.bulk(estf, reader, index='our-index')

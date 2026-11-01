"""Daily exchange rate history as CSV with the keyed API (160+ currencies).

Get a free API key at https://allratestoday.com/register and run:
  ALLRATES_API_KEY=... python history_keyed.py USD EUR 2026-01-01 2026-06-30 > usd_eur.csv
"""
import os
import sys
import urllib.request

src, dst, start, end = sys.argv[1:5]
url = (
    "https://allratestoday.com/api/v1/rates"
    f"?source={src}&target={dst}&from={start}&to={end}&format=csv"
)
req = urllib.request.Request(url, headers={"Authorization": f"Bearer {os.environ['ALLRATES_API_KEY']}"})
with urllib.request.urlopen(req, timeout=30) as res:
    sys.stdout.write(res.read().decode("utf-8-sig"))

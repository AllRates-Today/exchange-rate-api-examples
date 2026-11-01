"""Latest exchange rates in Python, standard library only, no API key.

Usage: python rates.py USD EUR 100
"""
import json
import sys
import urllib.request


def get_rates(base: str = "USD") -> dict:
    url = f"https://allratestoday.com/api/open/latest/{base.upper()}"
    req = urllib.request.Request(url, headers={"User-Agent": "exchange-rate-api-examples"})
    with urllib.request.urlopen(req, timeout=10) as res:
        return json.load(res)


def convert(amount: float, from_ccy: str, to_ccy: str) -> float:
    data = get_rates(from_ccy)
    return amount * data["rates"][to_ccy.upper()]


if __name__ == "__main__":
    args = sys.argv[1:]
    src = args[0] if len(args) > 0 else "USD"
    dst = args[1] if len(args) > 1 else "EUR"
    amt = args[2] if len(args) > 2 else "1"
    data = get_rates(src)
    rate = data["rates"][dst.upper()]
    print(f"{amt} {src} = {float(amt) * rate:.2f} {dst} (rate {rate}, {data['date']})")

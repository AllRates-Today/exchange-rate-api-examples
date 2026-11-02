# Exchange Rate API Examples

Copy-paste code for getting **currency exchange rates** in 11 languages and tools: curl, JavaScript, Node.js, React, Python, PHP, Go, Ruby, C#, Java and Excel.

Every example works the moment you copy it. **No API key, no sign-up, no dependencies.** It uses the free [AllRatesToday open endpoint](https://allratestoday.com/open-api/):

```
GET https://allratestoday.com/api/open/latest/{BASE}
```

- 30 major currencies (the European Central Bank reference table), re-based to any of them
- Updated every working day, CORS on, free for commercial use
- Need 160+ currencies, history or official central-bank rates? See [More than 30 currencies](#more-than-30-currencies)

## Contents

| Language / tool | File |
|---|---|
| [curl + jq](#curl) | [`curl/rates.sh`](curl/rates.sh) |
| [JavaScript (browser)](#javascript-browser) | [`javascript/browser.html`](javascript/browser.html) |
| [Node.js](#nodejs) | [`javascript/node.mjs`](javascript/node.mjs) |
| [React hook](#react) | [`react/useExchangeRates.js`](react/useExchangeRates.js) |
| [Python](#python) | [`python/rates.py`](python/rates.py) |
| [PHP](#php) | [`php/rates.php`](php/rates.php) |
| [Go](#go) | [`go/main.go`](go/main.go) |
| [Ruby](#ruby) | [`ruby/rates.rb`](ruby/rates.rb) |
| [C# / .NET](#c--net) | [`csharp/Program.cs`](csharp/Program.cs) |
| [Java](#java) | [`java/Rates.java`](java/Rates.java) |
| [Excel / Power BI](#excel--power-bi) | [`excel/power-query.m`](excel/power-query.m) |
| [Python: history as CSV (API key)](#more-than-30-currencies) | [`python/history_keyed.py`](python/history_keyed.py) |

## The response

```json
{
  "result": "success",
  "base_code": "USD",
  "date": "2026-10-30",
  "time_last_update_utc": "Fri, 30 Oct 2026 15:00:00 GMT",
  "time_next_update_utc": "Mon, 02 Nov 2026 15:00:00 GMT",
  "rates": {
    "USD": 1,
    "EUR": 0.89509488,
    "GBP": 0.74633011,
    "JPY": 157.25027,
    "INR": 94.955245
  }
}
```

To convert, multiply: `amount * rates[TO]`, with `FROM` as the base.

Currencies in the free table: AUD BRL CAD CHF CNY CZK DKK EUR GBP HKD HUF IDR ILS INR ISK JPY KRW MXN MYR NOK NZD PHP PLN RON SEK SGD THB TRY USD ZAR.

## curl

```bash
#!/usr/bin/env bash
# Latest exchange rates with curl + jq. No API key.
# Usage: ./rates.sh USD EUR 100
set -euo pipefail
FROM="${1:-USD}"; TO="${2:-EUR}"; AMOUNT="${3:-1}"

curl -s "https://allratestoday.com/api/open/latest/${FROM}" \
  | jq --arg to "$TO" --argjson amt "$AMOUNT" \
      '{date, from: .base_code, to: $to, rate: .rates[$to], result: (.rates[$to] * $amt)}'
```

## JavaScript (browser)

A full converter in one HTML file: [`javascript/browser.html`](javascript/browser.html). The core:

```js
const res = await fetch('https://allratestoday.com/api/open/latest/USD');
const { rates, date } = await res.json();
console.log(`100 USD = ${(100 * rates.EUR).toFixed(2)} EUR on ${date}`);
```

## Node.js

```js
// Latest exchange rates in Node.js 18+ (built-in fetch, no dependencies, no API key).
// Usage: node node.mjs USD EUR 100
const [from = 'USD', to = 'EUR', amount = '1'] = process.argv.slice(2);

const res = await fetch(`https://allratestoday.com/api/open/latest/${from}`);
if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
const data = await res.json();

const rate = data.rates[to];
if (rate === undefined) throw new Error(`${to} is not in the table`);

console.log(`${amount} ${from} = ${(Number(amount) * rate).toFixed(2)} ${to} (rate ${rate}, ${data.date})`);
```

## React

```js
// React hook: latest exchange rates for a base currency. No API key.
//
//   const { rates, date, error } = useExchangeRates('USD');
//   const eur = 100 * (rates?.EUR ?? 0);
//
// Show <a href="https://allratestoday.com">Exchange rates by AllRatesToday</a>
// on public pages that display the rates.
import { useEffect, useState } from 'react';

export function useExchangeRates(base = 'USD') {
  const [state, setState] = useState({ rates: null, date: null, error: null });

  useEffect(() => {
    const controller = new AbortController();
    fetch(`https://allratestoday.com/api/open/latest/${base}`, { signal: controller.signal })
      .then((res) => (res.ok ? res.json() : Promise.reject(new Error(`HTTP ${res.status}`))))
      .then((data) => setState({ rates: data.rates, date: data.date, error: null }))
      .catch((error) => {
        if (error.name !== 'AbortError') setState({ rates: null, date: null, error });
      });
    return () => controller.abort();
  }, [base]);

  return state;
}
```

## Python

```python
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
```

## PHP

```php
<?php
// Latest exchange rates in plain PHP (no Composer, no API key).
// Usage: php rates.php USD EUR 100
$from = $argv[1] ?? 'USD';
$to = $argv[2] ?? 'EUR';
$amount = (float) ($argv[3] ?? 1);

$json = file_get_contents("https://allratestoday.com/api/open/latest/" . urlencode($from));
if ($json === false) {
    exit("Request failed\n");
}
$data = json_decode($json, true);
$rate = $data['rates'][$to] ?? null;
if ($rate === null) {
    exit("$to is not in the table\n");
}

printf("%s %s = %.2f %s (rate %s, %s)\n", $amount, $from, $amount * $rate, $to, $rate, $data['date']);
```

## Go

```go
// Latest exchange rates in Go (standard library only, no API key).
// Usage: go run main.go USD EUR 100
package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"strconv"
)

type latest struct {
	BaseCode string             `json:"base_code"`
	Date     string             `json:"date"`
	Rates    map[string]float64 `json:"rates"`
}

func main() {
	from, to, amount := "USD", "EUR", 1.0
	if len(os.Args) > 2 {
		from, to = os.Args[1], os.Args[2]
	}
	if len(os.Args) > 3 {
		amount, _ = strconv.ParseFloat(os.Args[3], 64)
	}

	res, err := http.Get("https://allratestoday.com/api/open/latest/" + from)
	if err != nil {
		log.Fatal(err)
	}
	defer res.Body.Close()

	var data latest
	if err := json.NewDecoder(res.Body).Decode(&data); err != nil {
		log.Fatal(err)
	}
	rate, ok := data.Rates[to]
	if !ok {
		log.Fatalf("%s is not in the table", to)
	}
	fmt.Printf("%.2f %s = %.2f %s (rate %v, %s)\n", amount, from, amount*rate, to, rate, data.Date)
}
```

## Ruby

```ruby
# Latest exchange rates in Ruby (standard library only, no API key).
# Usage: ruby rates.rb USD EUR 100
require "json"
require "net/http"

from = ARGV[0] || "USD"
to = ARGV[1] || "EUR"
amount = (ARGV[2] || "1").to_f

data = JSON.parse(Net::HTTP.get(URI("https://allratestoday.com/api/open/latest/#{from}")))
rate = data.dig("rates", to) or abort("#{to} is not in the table")

puts format("%.2f %s = %.2f %s (rate %s, %s)", amount, from, amount * rate, to, rate, data["date"])
```

## C# / .NET

```csharp
// Latest exchange rates in C# (.NET 6+, no packages, no API key).
// Usage: dotnet run -- USD EUR 100
using System.Net.Http.Json;
using System.Text.Json.Serialization;

var from = args.Length > 0 ? args[0] : "USD";
var to = args.Length > 1 ? args[1] : "EUR";
var amount = args.Length > 2 ? decimal.Parse(args[2]) : 1m;

using var http = new HttpClient();
var data = await http.GetFromJsonAsync<Latest>($"https://allratestoday.com/api/open/latest/{from}")
           ?? throw new Exception("Empty response");

if (!data.Rates.TryGetValue(to, out var rate))
    throw new Exception($"{to} is not in the table");

Console.WriteLine($"{amount} {from} = {amount * rate:F2} {to} (rate {rate}, {data.Date})");

record Latest(
    [property: JsonPropertyName("base_code")] string BaseCode,
    [property: JsonPropertyName("date")] string Date,
    [property: JsonPropertyName("rates")] Dictionary<string, decimal> Rates);
```

## Java

```java
// Latest exchange rates in Java 11+ (no libraries, no API key).
// Usage: java Rates.java USD EUR 100
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Rates {
    public static void main(String[] args) throws Exception {
        String from = args.length > 0 ? args[0] : "USD";
        String to = args.length > 1 ? args[1] : "EUR";
        double amount = args.length > 2 ? Double.parseDouble(args[2]) : 1;

        HttpRequest req = HttpRequest.newBuilder(URI.create("https://allratestoday.com/api/open/latest/" + from)).build();
        String body = HttpClient.newHttpClient().send(req, HttpResponse.BodyHandlers.ofString()).body();

        // Use Jackson or Gson in a real app; a regex keeps this example dependency-free.
        Matcher m = Pattern.compile("\"" + to + "\":([0-9.eE+-]+)").matcher(body);
        if (!m.find()) throw new IllegalArgumentException(to + " is not in the table");
        double rate = Double.parseDouble(m.group(1));

        System.out.printf("%.2f %s = %.2f %s (rate %s)%n", amount, from, amount * rate, to, rate);
    }
}
```

## Excel / Power BI

```
// Excel / Power BI: Data > Get Data > From Other Sources > Blank Query > Advanced Editor.
// Paste this, change Base, then Close & Load. Refresh any time for the latest rates.
let
    Base = "USD",
    Source = Json.Document(Web.Contents("https://allratestoday.com/api/open/latest/" & Base)),
    Rates = Record.ToTable(Source[rates]),
    Renamed = Table.RenameColumns(Rates, {{"Name", "Currency"}, {"Value", "Rate"}}),
    Typed = Table.TransformColumnTypes(Renamed, {{"Rate", type number}}),
    WithDate = Table.AddColumn(Typed, "Date", each Source[date], type text)
in
    WithDate
```

## Attribution

If you show these rates on a **public web page, widget or public screen**, add a visible, normal link:

```html
<a href="https://allratestoday.com">Exchange rates by AllRatesToday</a>
```

Back-end use (invoices, reports, scheduled jobs, ERP syncs), libraries and private apps need no link. Full terms: [allratestoday.com/terms](https://allratestoday.com/terms/#attribution).

## More than 30 currencies

With a [free API key](https://allratestoday.com/register) the same idea covers much more:

| What | Request |
|---|---|
| 160+ currencies, live | `GET /api/v1/rates?source=USD&target=NGN,KES,PKR` |
| Convert an amount | `GET /api/v1/rates?source=USD&target=EUR&amount=1000` |
| A past date | `GET /api/v1/rates?source=USD&target=EUR&time=2026-06-30` |
| A date range | `GET /api/v1/rates?source=USD&target=EUR&from=2026-01-01&to=2026-06-30` |
| CSV, XML or Excel | add `&format=csv` (or `xml`, `xlsx`) |
| Official central bank rates (ECB, Fed, BoE, RBI, HMRC and 120+ more) | `GET /api/v1/central-bank/{bank}/latest` |

Send the key as `Authorization: Bearer YOUR_API_KEY`. Example: [`python/history_keyed.py`](python/history_keyed.py).

```python
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
```

## SDKs and other tools

- JavaScript / TypeScript: [`@allratestoday/sdk`](https://www.npmjs.com/package/@allratestoday/sdk)
- Python: [`allratestoday`](https://pypi.org/project/allratestoday/) · PHP: [`allratestoday/sdk`](https://packagist.org/packages/allratestoday/sdk) · Go: [`allratestoday-go`](https://github.com/AllRates-Today/allratestoday-go) · Rust: [`allratestoday`](https://crates.io/crates/allratestoday)
- Starter apps: [React converter](https://github.com/AllRates-Today/react-currency-converter) · [Next.js starter](https://github.com/AllRates-Today/nextjs-currency-starter) · [Google Sheets functions](https://github.com/AllRates-Today/google-sheets-exchange-rates) · [Python CLI](https://github.com/AllRates-Today/python-currency-cli)
- AI agents: [hosted MCP server](https://allratestoday.com/mcp/)

## Links

- Website: https://allratestoday.com
- Open endpoint docs: https://allratestoday.com/open-api/
- API documentation: https://allratestoday.com/developers/
- [ChatGPT app](https://chatgpt.com/plugins/plugin_asdk_app_6ae1e76098f48191a285ac3f5ab7a83b) — ask ChatGPT for live and official central bank rates
- All repositories: https://github.com/AllRates-Today

Found a bug or want another language? [Open an issue](https://github.com/AllRates-Today/exchange-rate-api-examples/issues) or send a pull request.

## License

MIT. See [LICENSE](LICENSE).

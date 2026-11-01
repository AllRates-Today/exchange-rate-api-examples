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

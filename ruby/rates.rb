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

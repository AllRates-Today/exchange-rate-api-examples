// Latest exchange rates in Node.js 18+ (built-in fetch, no dependencies, no API key).
// Usage: node node.mjs USD EUR 100
const [from = 'USD', to = 'EUR', amount = '1'] = process.argv.slice(2);

const res = await fetch(`https://allratestoday.com/api/open/latest/${from}`);
if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
const data = await res.json();

const rate = data.rates[to];
if (rate === undefined) throw new Error(`${to} is not in the table`);

console.log(`${amount} ${from} = ${(Number(amount) * rate).toFixed(2)} ${to} (rate ${rate}, ${data.date})`);

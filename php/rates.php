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

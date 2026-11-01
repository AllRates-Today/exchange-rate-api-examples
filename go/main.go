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

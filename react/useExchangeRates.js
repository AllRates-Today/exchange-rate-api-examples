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

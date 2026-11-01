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

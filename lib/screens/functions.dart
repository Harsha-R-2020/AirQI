import 'package:http/http.dart' as http;

fetchdata(String url) async {
  http.Response response = await http.get(Uri.parse(url));
  return response.body;
}
var flask_url = "http://192.168.1.11:8080";
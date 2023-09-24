import 'dart:convert';
import 'package:air_quality_app/screens/plotScreen.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:http/http.dart' as http;

class CityListWidget extends StatefulWidget {
  @override
  _CityListWidgetState createState() => _CityListWidgetState();
}

class _CityListWidgetState extends State<CityListWidget> {
  List<City> cities = [];

  @override
  void initState() {
    super.initState();
    fetchData();
  }

  Future<void> fetchData() async {
    try {
      final response = await http.get(Uri.parse('http://192.168.1.6:8080/getcities?query=a'));

      if (response.statusCode == 200) {
        final jsonResponse = json.decode(response.body);
        final citiesList = jsonResponse['message'] as List<dynamic>;

        setState(() {
          cities = citiesList.map((cityName) => City(name: cityName.toString())).toList();
        });
      } else {
        // Handle HTTP request error gracefully, e.g., show an error message.
        print('Failed to load data: ${response.statusCode}');
      }
    } catch (error) {
      // Handle other types of errors (e.g., network issues) here.
      print('Error: $error');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.white,
        title: Text('Top Polluted Cities'),
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              itemCount: cities.length,
              itemBuilder: (context, index) {
                final city = cities[index];
                return ListTile(
                  title: Text(city.name),
                );
              },

            ),
          ),
          Align(
            alignment: Alignment.bottomCenter,
            child: Padding(
              padding: EdgeInsets.all(50.0),
              child: GestureDetector(
                onTap: () {
                  // Add your onTap functionality here
                  HapticFeedback.lightImpact();
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) {
                        return MyPlot();
                      },
                    ),
                  );
                },
                child: Container(
                  width: 250,
                  height: 70,
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(50),
                    color: Colors.greenAccent,
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(
                        Icons.auto_graph_outlined, // You can replace this with your desired icon
                        color: Colors.white,   // Icon color
                        size: 30,              // Icon size
                      ),
                      SizedBox(width: 10), // Add some space between the icon and text
                      Text(
                        'View Plot',
                        style: TextStyle(
                          fontSize: 25,
                          color: Colors.white,
                        ),
                      ),
                    ],
                  ),
                ),
              )
            ),
          ),
        ],
      ),

    );
  }
}

class City {
  final String name;

  City({ this.name});
}

// void main() => runApp(MaterialApp(home: CityListWidget()));

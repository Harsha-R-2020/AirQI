import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:fluttertoast/fluttertoast.dart';

import '../const/colors.dart';
import 'aqiMeterScreen.dart';
import 'functions.dart';
import 'package:particles_flutter/particles_flutter.dart';

class PythonScreen extends StatefulWidget {
  // const PythonScreen({required Key key}) : super(key: key);

  @override
  _PythonScreenState createState() => _PythonScreenState();
}

class _PythonScreenState extends State<PythonScreen> {
  String url = '';
  var data;
  String output = 'Initial Output';
  String dropdownValue = 'Select City';
  @override
  Widget build(BuildContext context) {
    double h = MediaQuery.of(context).size.height;
    double w = MediaQuery.of(context).size.width;
    return Scaffold(
      appBar: AppBar(
          backgroundColor: Colors.white,
          centerTitle: true,

          title: Text("AQI Index")),
      body: Center(
        child: Container(
          padding: EdgeInsets.all(20),
          child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
            // TextField(
            //   onChanged: (value) {
            //     url = 'http://192.168.1.6:8080/api?query='+ value.toString();
            //   },
            // ),
            DropdownButton<String>(
              // Step 3.
              value: dropdownValue,
              // Step 4.
              items: <String>['Select City','Chennai', 'Delhi', 'Banglore', 'Mumbai']
                  .map<DropdownMenuItem<String>>((String value) {
                return DropdownMenuItem<String>(
                  value: value,
                  child: Text(
                    value,
                    style: TextStyle(fontSize: 30),
                  ),
                );
              }).toList(),
              // Step 5.
              onChanged: (String? newValue) {
                setState(() {
                  dropdownValue = newValue ?? 'Select City';
                });
              },
            ),
            TextButton(
                onPressed: () async {
                  url = 'http://192.168.1.8:8080/api?query='+ dropdownValue;
                  data = await fetchdata(url);
                  var decoded = jsonDecode(data);
                  setState(() {
                    output = decoded['message'];
                  });
                  if(output!="0"){
                    HapticFeedback.lightImpact();
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) {
                          return AQIMeter(speed: double.parse(output),option: dropdownValue);
                        },
                      ),
                    );
                  }
                  else{
                    Fluttertoast.showToast(
                        msg: 'Choose a valid city to proceed',
                        toastLength: Toast.LENGTH_SHORT,
                        gravity: ToastGravity.BOTTOM,
                        backgroundColor: Colors.red,
                        textColor: Colors.yellow
                    );
                  }
                  ;
                },
                child: Text(
                  'Find Air Quality Index',
                  style: TextStyle(fontSize: 20),
                )),
            Text(
              output,
              style: TextStyle(fontSize: 40, color: Colors.green),
            ),

          ]),
        ),
      ),
    );
  }
}
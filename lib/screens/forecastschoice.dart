import 'dart:convert';
import 'dart:math' as math;
import 'package:avatar_glow/avatar_glow.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:fluttertoast/fluttertoast.dart';

import '../const/colors.dart';
import 'aqiMeterScreen.dart';
import 'forecastedLSTMPlotsScreen.dart';
import 'forecastedPlotsScreen.dart';
import 'functions.dart';
import 'package:particles_flutter/particles_flutter.dart';

class ForecastChoiceScreen extends StatefulWidget {
  // const PythonScreen({required Key key}) : super(key: key);

  @override
  _ForecastChoiceScreenState createState() => _ForecastChoiceScreenState();
}

class _ForecastChoiceScreenState extends State<ForecastChoiceScreen> {
  String url = '';
  var data;
  String output = 'Initial Output';
  String dropdownValue = 'Select Model';

  @override
  Widget build(BuildContext context) {
    double h = MediaQuery.of(context).size.height;
    double w = MediaQuery.of(context).size.width;
    double _w = MediaQuery.of(context).size.width;
    return Scaffold(
      // appBar: AppBar(
      //     backgroundColor: Colors.white,
      //     centerTitle: true,
      //
      //     title: Text("AQI Index")),
      body: Stack(
        children: [
          CircularParticle(
            width: w,
            height: h,
            particleColor: Color((math.Random().nextDouble() * 0xFFFFFF).toInt()).withOpacity(0.2),
            numberOfParticles: 150,
            speedOfParticles: 0.5,
            maxParticleSize: 7,
            awayRadius: 0,
            onTapAnimation: false,
            isRandSize: true,
            isRandomColor: false,
            connectDots: false,
            enableHover: false,
          ),
          ListView(
            physics:
            BouncingScrollPhysics(parent: AlwaysScrollableScrollPhysics()),
            children: [

              Padding(
                padding: EdgeInsets.fromLTRB(_w / 17, _w / 20, 0, _w / 10),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'PM2.5 Forecasts',
                      style: TextStyle(
                        fontSize: 35,
                        color: Colors.black.withOpacity(.6),
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                    SizedBox(height: _w / 35),
                    Text(
                      'View Forecasted values of PM2.5 particle',
                      style: TextStyle(
                        fontSize: 17,
                        color: Colors.black.withOpacity(.5),
                        fontWeight: FontWeight.w500,
                      ),
                      textAlign: TextAlign.start,
                    ),
                  ],
                ),
              ),
              Container(
                child: Center(
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
                        items: <String>['Select Model','BiStackedLSTM(preferred)', 'XGBoost']
                            .map<DropdownMenuItem<String>>((String value) {
                          return DropdownMenuItem<String>(
                            value: value,
                            child: Text(
                              value,
                              style: TextStyle(fontSize: 22),
                            ),
                          );
                        }).toList(),
                        // Step 5.
                        onChanged: (String? newValue) {
                          setState(() {
                            dropdownValue = newValue ?? 'Select Model';
                          });
                        },
                      ),
                      Padding(
                          padding: EdgeInsets.all(55),
                          child: GestureDetector(
                            onTap: () async{
                              // Add your onTap functionality here
                              // url = flask_url+'/api?query='+ dropdownValue;
                              // data = await fetchdata(url);
                              // var decoded = jsonDecode(data);
                              // setState(() {
                              //   output = decoded['message'];
                              // });
                              if(dropdownValue=="XGBoost"){
                                HapticFeedback.lightImpact();
                                Navigator.push(
                                  context,
                                  MaterialPageRoute(
                                    builder: (context) {
                                      return ForecastedPlot();
                                    },
                                  ),
                                );
                              }
                              else if(dropdownValue=="BiStackedLSTM(preferred)"){
                                HapticFeedback.lightImpact();
                                Navigator.push(
                                  context,
                                  MaterialPageRoute(
                                    builder: (context) {
                                      return ForecastedLSTMPlot();
                                    },
                                  ),
                                );
                              }
                              else{
                                Fluttertoast.showToast(
                                    msg: 'Choose a option to proceed',
                                    toastLength: Toast.LENGTH_SHORT,
                                    gravity: ToastGravity.BOTTOM,
                                    backgroundColor: Colors.red,
                                    textColor: Colors.yellow
                                );
                              }
                              ;
                            },
                            child: Container(
                              width: 170,
                              height: 70,
                              decoration: BoxDecoration(
                                borderRadius: BorderRadius.circular(50),
                                color: Colors.deepOrangeAccent,
                              ),
                              child: Row(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Icon(
                                    Icons.speed_outlined, // You can replace this with your desired icon
                                    color: Colors.white,   // Icon color
                                    size: 35,              // Icon size
                                  ),
                                  SizedBox(width: 10), // Add some space between the icon and text
                                  Text(
                                    'Forecast',
                                    style: TextStyle(
                                      fontSize: 22,
                                      color: Colors.white,
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          )
                      ),
                      Center(
                        child: AvatarGlow(
                          glowColor: Colors.orangeAccent,
                          endRadius: 180,
                          duration: Duration(milliseconds: 2000),
                          repeat: true,
                          showTwoGlows: true,
                          curve: Curves.easeOutQuad,
                          child: Container(
                            height: 120,
                            width: 120,
                            decoration: BoxDecoration(
                                color: Colors.white, borderRadius: BorderRadius.circular(99)),
                            child: Icon(
                              Icons.analytics_sharp,
                              color: Colors.deepOrangeAccent,
                              size: 70,
                            ),
                          ),
                        ),
                        // TextButton(
                        //     onPressed: () async {
                        //       url = 'http://192.168.1.11:8080/api?query='+ dropdownValue;
                        //       data = await fetchdata(url);
                        //       var decoded = jsonDecode(data);
                        //       setState(() {
                        //         output = decoded['message'];
                        //       });
                        //       if(output!="0"){
                        //         HapticFeedback.lightImpact();
                        //         Navigator.push(
                        //           context,
                        //           MaterialPageRoute(
                        //             builder: (context) {
                        //               return AQIMeter(speed: double.parse(output),option: dropdownValue);
                        //             },
                        //           ),
                        //         );
                        //       }
                        //       else{
                        //         Fluttertoast.showToast(
                        //             msg: 'Choose a valid city to proceed',
                        //             toastLength: Toast.LENGTH_SHORT,
                        //             gravity: ToastGravity.BOTTOM,
                        //             backgroundColor: Colors.red,
                        //             textColor: Colors.yellow
                        //         );
                        //       }
                        //       ;
                        //     },
                        //     child: Text(
                        //       'Find Air Quality Index',
                        //       style: TextStyle(fontSize: 20),
                        //     )),
                        // Text(
                        //   output,
                        //   style: TextStyle(fontSize: 40, color: Colors.green),
                        // ),

                      ),
                      Padding(
                        padding: const EdgeInsets.all(8.0),
                        child: Text(
                          "Note : The forecasted values of the pm2.5 at delhi will be displayed as a plot and it may take some time to forecast the values while using LSTM model.",
                          style: TextStyle(
                            fontSize: 19,
                            color: Colors.black.withOpacity(.5),
                            fontWeight: FontWeight.w500,

                          ),
                          textAlign: TextAlign.justify,
                        ),
                      ),
                    ]),
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
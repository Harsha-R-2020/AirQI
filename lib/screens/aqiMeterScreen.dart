import 'package:air_quality_app/screens/plotScreen.dart';
import 'package:air_quality_app/screens/specificCleanPlot.dart';
import 'package:air_quality_app/screens/specificPollutedPlot.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:kdgaugeview/kdgaugeview.dart';
import 'package:particles_flutter/particles_flutter.dart';
import 'dart:math' as math;
import '../const/colors.dart';

class AQIMeter extends StatefulWidget {
  AQIMeter({required this.speed,required this.option});

  final double speed;
  final String option;

  @override
  _AQIMeterState createState() => _AQIMeterState();
}

class _AQIMeterState extends State<AQIMeter> {

  @override
  Widget build(BuildContext context) {
    SystemChrome.setSystemUIOverlayStyle(
        SystemUiOverlayStyle(
          statusBarColor:Colors.white, // <-- SEE HERE
          statusBarIconBrightness: Brightness.dark, //<-- For Android SEE HERE (dark icons)
          statusBarBrightness: Brightness.light, //<-- For iOS SEE HERE (dark icons)
        )
    );
    double h = MediaQuery.of(context).size.height;
    double _w = MediaQuery.of(context).size.width;
    return Scaffold(
      // appBar: AppBar(
      //   backgroundColor: Colors.white,
      //   centerTitle: true,
      //
      //   title: Text("AQI Meter"),
      // ),
      body: Stack(
        children: [
          Padding(
            padding: EdgeInsets.fromLTRB(_w / 17, _w / 8, 0, _w / 10),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'AQI Meter',
                  style: TextStyle(
                    fontSize: 37,
                    color: Colors.black.withOpacity(.6),
                    fontWeight: FontWeight.w700,
                  ),
                ),
                SizedBox(height: _w / 35),
                Text(
                  'View Realtime Air Quality Index',
                  style: TextStyle(
                    fontSize: 19,
                    color: Colors.black.withOpacity(.5),
                    fontWeight: FontWeight.w500,
                  ),
                  textAlign: TextAlign.start,
                ),
              ],
            ),
          ),
          CircularParticle(
            width: _w,
            height: h,
            particleColor: Color((math.Random().nextDouble() * 0xFFFFFF).toInt()).withOpacity(0.1),
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
          Center(
            child: Padding(
              padding: const EdgeInsets.all(15.0),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  Container(
                    width: 400,
                    height: 400,
                    padding: EdgeInsets.all(10),
                    child: KdGaugeView(
                      minSpeed: 0,
                      maxSpeed: 180,
                      speed: widget.speed,
                      animate: true,
                      duration: Duration(seconds: 5),
                      alertSpeedArray: [50, 90, 100],
                      alertColorArray: [Colors.orange, Colors.indigo, Colors.red],
                      unitOfMeasurement: "PPM",
                      gaugeWidth: 20,
                      fractionDigits: 1,
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
                                  return specificCleanMyPlot(option: widget.option);
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
                                  'View Cleansed Cities Plot',
                                  style: TextStyle(
                                    fontSize: 15,
                                    color: Colors.white,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        )
                    ),
                  ),
                  Align(
                    alignment: Alignment.bottomCenter,
                    child: Padding(
                        padding: EdgeInsets.all(0.5),
                        child: GestureDetector(
                          onTap: () {
                            // Add your onTap functionality here
                            HapticFeedback.lightImpact();
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (context) {
                                  return specificMyPlot(option: widget.option);
                                },
                              ),
                            );
                          },
                          child: Container(
                            width: 250,
                            height: 70,
                            decoration: BoxDecoration(
                              borderRadius: BorderRadius.circular(50),
                              color: Colors.redAccent,
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
                                  'View Polluted Cities Plot',
                                  style: TextStyle(
                                    fontSize: 15,
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
            ),
          ),
        ],
      ),
    );
  }
}
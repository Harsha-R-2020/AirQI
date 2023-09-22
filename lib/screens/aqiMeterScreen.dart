import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:kdgaugeview/kdgaugeview.dart';

import '../const/colors.dart';

class AQIMeter extends StatefulWidget {
  AQIMeter({Key key, this.speed}) : super(key: key);

  final double speed;

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
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.white,
        centerTitle: true,

        title: Text("AQI Meter"),
      ),
      body: Center(
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
            )
          ],
        ),
      ),
    );
  }
}
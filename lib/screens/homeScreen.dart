import 'package:air_quality_app/screens/plotScreen.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:particles_flutter/particles_flutter.dart';
import 'dart:ui';

import '../main.dart';
import 'DisplayCitiesBad.dart';
import 'Mapscreen.dart';
import 'aqiMeterScreen.dart';
import 'chatbot.dart';
import 'forecastedPlotsScreen.dart';
import 'goodPlotsScreen.dart';
import 'pythonScreen.dart';

class MyCustomUI extends StatefulWidget {
  @override
  _MyCustomUIState createState() => _MyCustomUIState();
}

class _MyCustomUIState extends State<MyCustomUI>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;
  late Animation<double> _animation2;

  @override
  void initState() {
    super.initState();

    _controller = AnimationController(
      vsync: this,
      duration: Duration(seconds: 1),
    );

    _animation = Tween<double>(begin: 0, end: 1)
        .animate(CurvedAnimation(parent: _controller, curve: Curves.easeOut))
      ..addListener(() {
        setState(() {});
      });

    _animation2 = Tween<double>(begin: -30, end: 0)
        .animate(CurvedAnimation(parent: _controller, curve: Curves.easeOut));

    _controller.forward();
    _controller.forward();
  }

  @override
  void dispose() {
    _controller.dispose();
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    double _w = MediaQuery.of(context).size.width;
    SystemChrome.setSystemUIOverlayStyle(
        SystemUiOverlayStyle(
          statusBarColor: Colors.white, // <-- SEE HERE
          statusBarIconBrightness: Brightness.dark, //<-- For Android SEE HERE (dark icons)
          statusBarBrightness: Brightness.light, //<-- For iOS SEE HERE (dark icons)
        )
    );
    double h = MediaQuery.of(context).size.height;
    double w = MediaQuery.of(context).size.width;
    return Scaffold(
      backgroundColor: Colors.white,
      body: Stack(
        children: [
          /// ListView
      Stack(
      children: [
      CircularParticle(
      width: w,
        height: h,
        particleColor: Colors.blueAccent.withOpacity(.2),
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
                      'AirQI',
                      style: TextStyle(
                        fontSize: 37,
                        color: Colors.black.withOpacity(.6),
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                    SizedBox(height: _w / 35),
                    Text(
                      'Air Quality prediction app.',
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
              homePageCard(
                Color(0xfff37736),
                Icons.analytics_outlined,
                'PM2.5 Forecasting',
                context,
                ForecastedPlot(),
              ),
              homePageCard(
                Colors.lightBlue,
                Icons.speed_outlined,
                'View Air Quality Index',
                context,
                PythonScreen(),
              ),
              homePageCard(
                Colors.redAccent,
                Icons.auto_graph_outlined,
                'View Top Polluted Cities',
                context,
                MyPlot(),
              ),
              homePageCard(
                Colors.lightGreen,
                Icons.auto_graph_outlined,
                'View Top Cleansed Cities',
                context,
                GoodPlot(),
              ),
              homePageCard(
                Colors.lightGreen,
                Icons.chat_outlined,
                'Chatbot',
                context,
                chatbotScreen(),
              ),
              // homePageCardsGroup(
              //     Colors.lightGreen,
              //     Icons.gamepad_outlined,
              //     'Example example',
              //     context,
              //     RouteWhereYouGo(),
              //     Color(0xffffa700),
              //     Icons.article,
              //     'Example example',
              //     RouteWhereYouGo()),
              // homePageCardsGroup(
              //     Color(0xff63ace5),
              //     Icons.ad_units_outlined,
              //     'Example example example',
              //     context,
              //     RouteWhereYouGo(),
              //     Color(0xfff37736),
              //     Icons.article_sharp,
              //     'Example example',
              //     RouteWhereYouGo()),
              // homePageCardsGroup(
              //     Color(0xffFF6D6D),
              //     Icons.android,
              //     'Example example',
              //     context,
              //     RouteWhereYouGo(),
              //     Colors.lightGreen,
              //     Icons.text_format,
              //     'Example',
              //     RouteWhereYouGo()),
              // homePageCardsGroup(
              //     Color(0xffffa700),
              //     Icons.text_fields,
              //     'Example',
              //     context,
              //     RouteWhereYouGo(),
              //     Color(0xff63ace5),
              //     Icons.calendar_today_sharp,
              //     'Example example',
              //     RouteWhereYouGo()),
              SizedBox(height: _w / 20),
            ],
          ),

          /// SETTING ICON
          Padding(
            padding: EdgeInsets.fromLTRB(0, _w / 9.5, _w / 15, 0),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                InkWell(
                  highlightColor: Colors.transparent,
                  splashColor: Colors.transparent,
                  onTap: () {
                    HapticFeedback.lightImpact();
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) {
                          return RouteWhereYouGo();
                        },
                      ),
                    );
                  },
                  child: ClipRRect(
                    borderRadius: BorderRadius.all(Radius.circular(99)),
                    child: BackdropFilter(
                      filter: ImageFilter.blur(sigmaY: 5, sigmaX: 5),
                      child: Container(
                        height: _w / 6.5,
                        width: _w / 8.5,
                        decoration: BoxDecoration(
                          color: Colors.black.withOpacity(.05),
                          shape: BoxShape.circle,
                        ),
                        child: Center(
                          child: Icon(
                            Icons.info,
                            size: _w / 17,
                            color: Colors.black.withOpacity(.6),
                          ),
                        ),
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),

          // Blur the Status bar
          blurTheStatusBar(context),
        ],
      ),
    ]
      )
    );
  }

  Widget homePageCardsGroup(
      Color color,
      IconData icon,
      String title,
      BuildContext context,
      Widget route,
      Color color2,
      IconData icon2,
      String title2,
      Widget route2) {
    double _w = MediaQuery.of(context).size.width;
    return Padding(
      padding: EdgeInsets.only(bottom: _w / 17),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          homePageCard(color, icon, title, context, route),
          homePageCard(color2, icon2, title2, context, route2),
        ],
      ),
    );
  }

  Widget homePageCard(Color color, IconData icon, String title,
      BuildContext context, Widget route) {
    double _w = MediaQuery.of(context).size.width;
    return Padding(
      padding: const EdgeInsets.all(20.0),
      child: Opacity(
        opacity: _animation.value,
        child: Transform.translate(
          offset: Offset(0, _animation2.value),
          child: InkWell(
            highlightColor: Colors.transparent,
            splashColor: Colors.transparent,
            onTap: () {
              HapticFeedback.lightImpact();
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) {
                    return route;
                  },
                ),
              );
            },
            child: Container(
              padding: EdgeInsets.all(15),
              height: _w / 2,
              width: _w / 2.4,
              decoration: BoxDecoration(
                color: Colors.white,
                boxShadow: [
                  BoxShadow(
                    color: Color(0xff040039).withOpacity(.15),
                    blurRadius: 99,
                  ),
                ],
                borderRadius: BorderRadius.all(
                  Radius.circular(25),
                ),
              ),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  SizedBox(),
                  Container(
                    height: _w / 5,
                    width: _w / 5,
                    decoration: BoxDecoration(
                      color: color.withOpacity(.1),
                      shape: BoxShape.circle,
                    ),
                    child: Icon(
                      icon,
                      size: _w/7,
                      color: color.withOpacity(.6),
                    ),
                  ),
                  Text(
                    title,
                    maxLines: 4,
                    softWrap: true,
                    overflow: TextOverflow.ellipsis,
                    style: TextStyle(
                      fontSize: 18,
                      color: Colors.black.withOpacity(.5),
                      fontWeight: FontWeight.w700,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  SizedBox(),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget blurTheStatusBar(BuildContext context) {
    double _w = MediaQuery.of(context).size.width;
    return ClipRRect(
      child: BackdropFilter(
        filter: ImageFilter.blur(sigmaY: 5, sigmaX: 5),
        child: Container(
          height: _w / 18,
          color: Colors.transparent,
        ),
      ),
    );
  }
}

class RouteWhereYouGo extends StatelessWidget {

  @override
  Widget build(BuildContext context) {
    double h = MediaQuery.of(context).size.height;
    double w = MediaQuery.of(context).size.width;
    double _w = MediaQuery.of(context).size.width;
    return  Scaffold(
      backgroundColor: Colors.white,
      body: Stack(
        children: [
      /// ListView
      Stack(
      children: [
      CircularParticle(
      width: w,
        height: h,
        particleColor: Colors.blueAccent.withOpacity(.2),
        numberOfParticles: 150,
        speedOfParticles: 0.5,
        maxParticleSize: 7,
        awayRadius: 0,
        onTapAnimation: true,
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
                'About ',
                style: TextStyle(
                  fontSize: 37,
                  color: Colors.black.withOpacity(.6),
                  fontWeight: FontWeight.w700,
                ),
              ),
              SizedBox(height: _w / 35),
              Text(
                'Air Quality prediction app.',
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
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Text(
                'Your Air Quality Companion ',
                style: TextStyle(
                  fontSize: 23,
                  color: Colors.black.withOpacity(.6),
                  fontWeight: FontWeight.w700,
                ),
              ),
            ),
            SizedBox(height: _w / 35),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Text(
                "AirQI is your go-to app for staying informed about the air you breathe."
                    " We believe that everyone deserves to know the quality of the air around them, "
                    "and we're here to provide you with real-time data on air quality, empowering you "
                    "to make healthier choices for yourself and your community.",
                style: TextStyle(
                  fontSize: 19,
                  color: Colors.black.withOpacity(.5),
                  fontWeight: FontWeight.w500,

                ),
                textAlign: TextAlign.justify,
              ),
            ),
            SizedBox(height: _w / 35),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Text(
                'Live AQI Data ',
                style: TextStyle(
                  fontSize: 23,
                  color: Colors.black.withOpacity(.6),
                  fontWeight: FontWeight.w700,
                ),
              ),
            ),
            SizedBox(height: _w / 35),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Text(
                "With AirQI, you can access up-to-the-minute Air Quality Index (AQI) data for your location. "
                    "We pull data from reliable sources to ensure you always have the latest information on "
                    "air quality conditions in your area.",
                style: TextStyle(
                  fontSize: 19,
                  color: Colors.black.withOpacity(.5),
                  fontWeight: FontWeight.w500,

                ),
                textAlign: TextAlign.justify,
              ),
            ),
            SizedBox(height: _w / 35),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Text(
                'Top Polluted Cities',
                style: TextStyle(
                  fontSize: 23,
                  color: Colors.black.withOpacity(.6),
                  fontWeight: FontWeight.w700,
                ),
              ),
            ),
            SizedBox(height: _w / 35),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Text(
                "Stay informed about the most polluted cities around the world. AirQI ranks cities based on their AQI, "
                    "helping you plan your travels or simply satisfy your curiosity about air quality in different places.",
                style: TextStyle(
                  fontSize: 19,
                  color: Colors.black.withOpacity(.5),
                  fontWeight: FontWeight.w500,

                ),
                textAlign: TextAlign.justify,
              ),
            ),
            SizedBox(height: _w / 35),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Text(
                'Top Clean Cities',
                style: TextStyle(
                  fontSize: 23,
                  color: Colors.black.withOpacity(.6),
                  fontWeight: FontWeight.w700,
                ),
              ),
            ),
            SizedBox(height: _w / 35),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Text(
                "On the flip side, we also celebrate cities with the cleanest air. "
                    "Discover which cities boast the freshest, healthiest air, "
                    "and perhaps find your next vacation destination or relocation spot.",
                style: TextStyle(
                  fontSize: 19,
                  color: Colors.black.withOpacity(.5),
                  fontWeight: FontWeight.w500,

                ),
                textAlign: TextAlign.justify,
              ),
            ),
            SizedBox(height: _w / 35),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Text(
                'User-Friendly Interface',
                style: TextStyle(
                  fontSize: 23,
                  color: Colors.black.withOpacity(.6),
                  fontWeight: FontWeight.w700,
                ),
              ),
            ),
            SizedBox(height: _w / 35),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Text(
                " AirQI is designed with you in mind. "
                    "Our user-friendly interface makes it easy to access and understand air quality data,"
                    " even for those new to the topic",
                style: TextStyle(
                  fontSize: 19,
                  color: Colors.black.withOpacity(.5),
                  fontWeight: FontWeight.w500,

                ),
                textAlign: TextAlign.justify,
              ),
            ),
            SizedBox(height: _w / 35),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Text(
                'Why AirQI?',
                style: TextStyle(
                  fontSize: 23,
                  color: Colors.black.withOpacity(.6),
                  fontWeight: FontWeight.w700,
                ),
              ),
            ),
            SizedBox(height: _w / 35),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Text(
                "At AirQI, we are committed to making air quality information accessible and actionable for everyone. We understand that clean air is essential for a healthy life, and we believe that knowledge is the first step toward positive change."

   "Whether you're planning outdoor activities, considering a move to a new city, or just want to stay informed about the air you breathe daily, AirQI is your trusted companion. Join us in the quest for better air quality, one informed choice at a time."

    "Download AirQI today and take control of the air you breathe. Your health and well-being deserve nothing less.",
                style: TextStyle(
                  fontSize: 19,
                  color: Colors.black.withOpacity(.5),
                  fontWeight: FontWeight.w500,

                ),
                textAlign: TextAlign.justify,
              ),
            ),
            SizedBox(height: _w / 35),


    ])
    ])
    ])
    );
  }
}
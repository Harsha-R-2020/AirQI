import 'package:flutter/material.dart';
import 'package:flutter_displaymode/flutter_displaymode.dart';


import './screens/spashScreen.dart';

import './const/colors.dart';


void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await FlutterDisplayMode.setHighRefreshRate();
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AirQI',
      theme: ThemeData(
        fontFamily: "Metropolis",
        primarySwatch: Colors.lightBlue,
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ButtonStyle(
            backgroundColor: MaterialStateProperty.all(
              AppColor.orange,
            ),
            shape: MaterialStateProperty.all(
              StadiumBorder(),
            ),
            elevation: MaterialStateProperty.all(0),
          ),
        ),
        textButtonTheme: TextButtonThemeData(
          style: ButtonStyle(
            foregroundColor: MaterialStateProperty.all(
              AppColor.orange,
            ),
          ),
        ),
        textTheme: TextTheme(
          headline3: TextStyle(
            color: AppColor.primary,
            fontSize: 16,
            fontWeight: FontWeight.bold,
          ),
          headline4: TextStyle(
            color: AppColor.secondary,
            fontWeight: FontWeight.bold,
            fontSize: 20,
          ),
          headline5: TextStyle(
            color: AppColor.primary,
            fontWeight: FontWeight.normal,
            fontSize: 25,
          ),
          headline6: TextStyle(
            color: AppColor.primary,
            fontSize: 25,
          ),
          bodyText2: TextStyle(
            color: AppColor.secondary,
          ),
        ),
      ),
      home: MyCustomWidget(),
      // routes: {
      //   LandingScreen.routeName: (context) => LandingScreen(),
      //   LoginScreen.routeName: (context) => LoginScreen(),
      //   SignUpScreen.routeName: (context) => SignUpScreen(),
      //   ForgetPwScreen.routeName: (context) => ForgetPwScreen(),
      //   SendOTPScreen.routeName: (context) => SendOTPScreen(),
      //   NewPwScreen.routeName: (context) => NewPwScreen(),
      //   IntroScreen.routeName: (context) => IntroScreen(),
      // },
    );
  }
}

import 'dart:convert';
import 'dart:math' as math;
import 'package:avatar_glow/avatar_glow.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:particles_flutter/particles_flutter.dart';
import 'dart:typed_data';
import 'package:photo_view/photo_view.dart';
import 'package:animator/animator.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import 'functions.dart';

// void main() => runApp(MyApp());

class specificCleanMyPlot extends StatelessWidget {
  specificCleanMyPlot({required this.option});
  final String option;
  @override
  Widget build(BuildContext context) {
    double _w = MediaQuery.of(context).size.width;
    return Scaffold(
      // appBar: AppBar(
      //   backgroundColor: Colors.white,
      //   centerTitle: true,
      //   title:  Text("Top Polluted cities",style: TextStyle(
      //     fontSize: _w / 17,
      //     color: Colors.black,
      //   ),),
      // ),
      body:
      ImageFromAPI(option: option),

    );
  }
}

// class TextFromAPI extends StatefulWidget {
//   @override
//   _TextFromAPIState createState() => _TextFromAPIState();
// }
//
// class _TextFromAPIState extends State<TextFromAPI> {
//   String url = 'http://192.168.137.87:8080/getcities?query=a'; // Replace with your Flask API URL
//   var rslt=["","",""];
//     Future<void> fetchImage() async {
//       var data = await fetchdata(url);
//       var decoded = jsonDecode(data);
//       setState(() {
//         rslt = decoded['message'];
//       });
//     }
//
//     @override
//     void initState() {
//       super.initState();
//       fetchImage();
//     }
//   @override
//   Widget build(BuildContext context) {
//     double _w = MediaQuery.of(context).size.width;
//       return Container(
//           padding: EdgeInsets.all(20),
//           width: _w/5, // Set the desired width
//           height: _w/5,
//         child: Text(rslt[0]+"\n"+rslt[1]+"\n"+rslt[2]+"\n",
//               style: TextStyle(
//               fontSize: _w / 17,
//               color: Colors.black.withOpacity(.7),
//               fontWeight: FontWeight.w400,
//         ),
//       )
//       );
//   }
//
// }
class ImageFromAPI extends StatefulWidget {
  ImageFromAPI({required this.option});
  final String option;
  @override
  _ImageFromAPIState createState() => _ImageFromAPIState();
}

class _ImageFromAPIState extends State<ImageFromAPI> {
  // Replace with your Flask API URL

  Future<void> fetchImage() async {
    String imageUrl = flask_url+'/specificcleanplot?query='+widget.option;

    final response = await http.get(Uri.parse(imageUrl));
    if (response.statusCode == 200) {
      // Image retrieved successfully
      setState(() {
        // Set the image data to a Uint8List and update the UI
        // This assumes you are receiving a JPEG image
        // Modify this part if your image format is different
        imageBytes = response.bodyBytes;
        loading = false;
      });
    } else {
      // Handle error, e.g., display a placeholder image
      print('Failed to load image: ${response.statusCode}');
    }
  }
  late Uint8List? imageBytes;
  bool loading = true;

  @override
  void initState() {
    super.initState();
    fetchImage();
  }

  @override
  Widget build(BuildContext context) {
    double _w = MediaQuery.of(context).size.width;
    double h = MediaQuery.of(context).size.height;
    return Stack(
      children: [
        CircularParticle(
          width: _w,
          height: h,
          particleColor:Colors.lightGreen.withOpacity(0.2),
          numberOfParticles: 150,
          speedOfParticles: 0.5,
          maxParticleSize: 7,
          awayRadius: 0,
          onTapAnimation: true,
          isRandSize: true,
          isRandomColor: false,
          connectDots: false,
          enableHover: true,
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
                      'Insights',
                      style: TextStyle(
                        fontSize: 37,
                        color: Colors.black.withOpacity(.6),
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                    SizedBox(height: _w / 35),
                    Text(
                      'Top Cleansed Areas.',
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

              Center(
                child: Container(
                  padding: EdgeInsets.all(20),
                  width: _w, // Set the desired width
                  height: _w,
                  child: loading != true
                      ? GestureDetector(
                    child: PhotoView(
                      imageProvider: MemoryImage(imageBytes!),
                      backgroundDecoration: BoxDecoration(
                        color: Colors.white, // Change the background color
                      ),
                      minScale: PhotoViewComputedScale.contained * 0.8, // Set min scale
                      maxScale: PhotoViewComputedScale.covered * 2.0,

                    ),
                  )
                      : MyCustomLoadingWidget(),
                ),
                // Display a loading indicator
              ),
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: Text(
                  "Note : The AQI data is retrieved in real-time, so please be patient as it may take a moment to load.",
                  style: TextStyle(
                    fontSize: 19,
                    color: Colors.black.withOpacity(.5),
                    fontWeight: FontWeight.w500,

                  ),
                  textAlign: TextAlign.justify,
                ),
              ),

            ]
        )
      ],
    );
  }
}
class MyCustomLoadingWidget extends StatefulWidget {
  @override
  _MyCustomLoadingWidgetState createState() => _MyCustomLoadingWidgetState();
}

class _MyCustomLoadingWidgetState extends State<MyCustomLoadingWidget> {
  @override
  Widget build(BuildContext context) {
    double _w = MediaQuery.of(context).size.width;
    return Scaffold(
      // body: Center(
      //   child: Container(
      //     height: _w/2,
      //     width: _w/2,
      //     child: Animator<double>(
      //       duration: Duration(milliseconds: 1500),
      //       cycles: 0,
      //       curve: Curves.easeInOut,
      //       tween: Tween<double>(begin: 0.0, end: 15.0),
      //       builder: (context, animatorState, child) => Container(
      //         margin: EdgeInsets.all(animatorState.value),
      //         decoration: BoxDecoration(
      //           shape: BoxShape.circle,
      //           color: Color(0xFFFF5757),
      //           boxShadow: [
      //             BoxShadow(
      //               color: Color(0xFFFF5757).withOpacity(0.5),
      //               offset: Offset(0, 5),
      //               blurRadius: 30,
      //             ),
      //           ],
      //         ),
      //         child: Center(
      //           child: Icon(
      //             Icons.auto_graph_outlined,
      //             color: Colors.white,
      //             size: 100,
      //           ),
      //         ),
      //       ),
      //     ),
      //   ),
      // ),
      body: Center(
        child: AvatarGlow(
          glowColor: Colors.lightGreen.withOpacity(0.5),
          endRadius: _w/2,
          duration: Duration(milliseconds: 2000),
          repeat: true,
          showTwoGlows: true,
          curve: Curves.easeOutQuad,
          child: Container(
            height: _w/2.5,
            width: _w/2.5,
            decoration: BoxDecoration(
                color: Colors.lightGreen, borderRadius: BorderRadius.circular(99)),
            child: Icon(
              Icons.auto_graph_outlined,
              color: Colors.white,
              size: 40,
            ),
          ),
        ),
      ),
    );
  }
}


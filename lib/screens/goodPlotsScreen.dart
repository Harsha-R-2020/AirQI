import 'package:animator/animator.dart';
import 'package:avatar_glow/avatar_glow.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:typed_data';

import 'package:photo_view/photo_view.dart';


// void main() => runApp(MyApp());

class GoodPlot extends StatelessWidget {

  @override
  Widget build(BuildContext context) {
    double _w = MediaQuery.of(context).size.width;
    return Scaffold(
      // appBar: AppBar(
      //   backgroundColor: Colors.white,
      //   centerTitle: true,
      //   title:  Text("Top Cleansed cities",style: TextStyle(
      //     fontSize: _w / 17,
      //     color: Colors.black,
      //   ),),
      // ),
      body: GoodImageFromAPI(),
    );
  }
}

class GoodImageFromAPI extends StatefulWidget {
  @override
  _GoodImageFromAPIState createState() => _GoodImageFromAPIState();
}

class _GoodImageFromAPIState extends State<GoodImageFromAPI> {
  String imageUrl = 'http://192.168.1.6:8080/goodplot?query=a'; // Replace with your Flask API URL

  Future<void> fetchImage() async {
    final response = await http.get(Uri.parse(imageUrl));
    if (response.statusCode == 200) {
      // Image retrieved successfully
      setState(() {
        // Set the image data to a Uint8List and update the UI
        // This assumes you are receiving a JPEG image
        // Modify this part if your image format is different
        imageBytes = response.bodyBytes;
      });
    } else {
      // Handle error, e.g., display a placeholder image
      print('Failed to load image: ${response.statusCode}');
    }
  }

  Uint8List imageBytes;

  @override
  void initState() {
    super.initState();
    fetchImage();
  }

  @override
  Widget build(BuildContext context) {
    double _w = MediaQuery.of(context).size.width;
    return Stack(
        children: [
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
                'Top Cleansed Cities in TamilNadu',
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
                      child: imageBytes != null
                          ? GestureDetector(
                                child: PhotoView(
                                  imageProvider: MemoryImage(imageBytes),
                                  backgroundDecoration: BoxDecoration(
                                    color: Colors.white, // Change the background color
                                  ),
                                  minScale: PhotoViewComputedScale.contained * 0.8, // Set min scale
                                  maxScale: PhotoViewComputedScale.covered * 2.0,
                        ),
                      )
                          : MyCustomLoadingWidget(),
                    ), // Display a loading indicator
                  )
    ]
    )
    ]);
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
      body: Center(
        child:  AvatarGlow(
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
                color:  Colors.lightGreen, borderRadius: BorderRadius.circular(99)),
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


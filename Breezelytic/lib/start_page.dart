import 'package:flutter/material.dart';
import 'package:breezelytic/currentdata.dart';
import 'package:breezelytic/records.dart';

class StartPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Breezelytic",
          style: TextStyle(fontSize: 25, fontWeight: FontWeight.w400)),
        centerTitle: true,
        toolbarHeight: 60,
        toolbarOpacity: 0.9,
        shape: const RoundedRectangleBorder(
          borderRadius: BorderRadius.only(
              bottomRight: Radius.circular(25),
              bottomLeft: Radius.circular(25)
          ),
        ),
        backgroundColor: Colors.blueAccent[400],
        foregroundColor: Colors.white,
      ),
      body: Center(
        child: SafeArea(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            children: [
               Image.asset('assets/logo.png', width: 500, height: 500),

              Row(
                children: [
                  SizedBox(width: 70),
              ElevatedButton(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => CurrentData()),
                  );
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.blueAccent,
                ),
                child: Text(
                  'Current AQI',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 20,
                  ),
                ),
              ),
                  SizedBox(width: 10),
              ElevatedButton(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => FetchRecords()),
                  );
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.blueAccent,
                ),
                child: Text(
                  'AQI Records',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 20,
                  ),
                ),
              ),
                  ]
              )
            ],
          ),
        ),
      ),
    );
  }
}

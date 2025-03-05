import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class CurrentData extends StatefulWidget {
  @override
  _CurrentDataState createState() => _CurrentDataState();
}

class _CurrentDataState extends State<CurrentData> {
  String locationValue = 'Hyderabad';
  int pm25Value = 0;

  List<String> locations = ['Hyderabad', 'Delhi'];

  Future<void> fetchDataFromAPI(String location) async {
    final response = await http.get(

    Uri.parse('http://10.0.2.2:8000/sendtoApp?location=$location')
    ,
    );

    if (response.statusCode == 200) {
      var data = json.decode(response.body);
      print(data);

      if (data['status'] == 'ok') {
        setState(() {
          String Fetchedlocation = data['data']['city']['name'];
          if(Fetchedlocation.contains('Hyderabad')){
            locationValue ='Hyderabad';
          }
          else if(Fetchedlocation.contains('Delhi')){
            locationValue ='Delhi';
          }

          pm25Value = data['data']['forecast']['daily']['pm25'][2]['avg'];
        });
      } else {
        setState(() {
          locationValue = 'Error';
          pm25Value = 0;
        });
      }
    } else {
      setState(() {
        locationValue = 'Error';
        pm25Value = 0;
      });
    }
  }

  @override
  void initState() {
    super.initState();
    fetchDataFromAPI(locationValue);
  }

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
              SizedBox(height: 90,),
              Image.asset('assets/logo.png', width: 500, height: 500),
              SizedBox(height: 10,),

              Text('Location: $locationValue',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.w400),

        ),
              Text('PM25 Value: $pm25Value',
                  style: TextStyle(fontSize: 20, fontWeight: FontWeight.w400),
        ),
              SizedBox(height: 20),
              DropdownButton<String>(
                value: locationValue,
                iconEnabledColor: Colors.blueAccent,
                onChanged: (String? newLocation) {
                  if (newLocation != null) {
                    fetchDataFromAPI(newLocation);
                  }
                },
                items: locations.map<DropdownMenuItem<String>>((String location) {
                  return DropdownMenuItem<String>(
                    value: location,
                    child: Text(location),
                  );
                }).toList(),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

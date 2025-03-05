import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class FetchRecords extends StatefulWidget {
  const FetchRecords({super.key});

  @override
  State<FetchRecords> createState() => _FetchRecordsState();
}

class _FetchRecordsState extends State<FetchRecords> {
  List<Map<String, dynamic>> records = [];

  @override
  void initState() {
    super.initState();
    fetchData();
  }

  Future<void> fetchData() async {
    final response =
        await http.get(Uri.parse('http://10.0.2.2:8000/fetchrecords'));

    if (response.statusCode == 200) {
      print("success!!---------------");
      List<dynamic> data = json.decode(response.body);

      setState(() {
        records = data
            .map((record) => {
                  "date": record['date'].toString(),
                  "avg_pm25": record['avg_pm25'].toString(),
                  "max_pm25": record['max_pm25'].toString(),
                  "min_pm25": record['min_pm25'].toString(),
                })
            .toList();
      });
    } else {
      print('failed to fetch data :(');
      print(response.statusCode );
    }
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
      body: records.isEmpty
          ? const Center(child: CircularProgressIndicator())
          : ListView.builder(
              itemCount: records.length,
              itemBuilder: (context, index) {
                final record = records[index];
                return Card(
                  margin: const EdgeInsets.all(10),
                  child: ListTile(
                    title: Text("Date: ${record['date']}"),
                    subtitle: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text("Avg PM2.5: ${record['avg_pm25']}"),
                        Text("Max PM2.5: ${record['max_pm25']}"),
                        Text("Min PM2.5: ${record['min_pm25']}"),
                      ],
                    ),
                  ),
                );
              },
            ),
    );
  }
}

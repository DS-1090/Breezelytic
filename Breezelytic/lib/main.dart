import 'package:breezelytic/start_page.dart';
import 'package:flutter/material.dart';
import 'package:breezelytic/records.dart';
void main() {
  runApp(const MyApp());
}
//root window
class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(

        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue.shade200),
        useMaterial3: true,
      ),
      home: StartPage(),
    );
  }
}
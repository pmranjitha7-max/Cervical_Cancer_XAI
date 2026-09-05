// Basic smoke test: the app should build and show the splash screen's
// brand mark without throwing.
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:cervixai/main.dart';

void main() {
  testWidgets('App launches and shows the CerviXAI brand on splash', (WidgetTester tester) async {
    await tester.pumpWidget(const CervixAiApp());
    await tester.pump();

    expect(find.text('CerviXAI'), findsOneWidget);
  });
}

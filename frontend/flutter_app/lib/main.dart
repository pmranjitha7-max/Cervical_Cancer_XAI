import 'dart:convert';
import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

const apiUrl = String.fromEnvironment(
  'API_BASE_URL',
  defaultValue: 'http://10.130.181.238:8000',
);
void main() => runApp(const CervixAi());

class S {
  static final i = S();
  String name = 'Healthcare Professional', user = '', email = '', pass = '';
  final history = <H>[];
}

class H {
  H(this.id, this.result, this.risk, this.date);
  final int id;
  final String result;
  final double risk;
  final DateTime date;
}

class C {
  static const navy = Color(0xff102a43),
      blue = Color(0xff276ef1),
      cyan = Color(0xff35b8c8),
      mint = Color(0xff54d6b6),
      red = Color(0xffdf5264),
      muted = Color(0xff687d91);
}

class CervixAi extends StatelessWidget {
  const CervixAi({super.key});
  @override
  Widget build(BuildContext c) => MaterialApp(
          debugShowCheckedModeBanner: false,
          title: 'CerviXAI',
          theme: ThemeData(
              useMaterial3: true,
              colorScheme: ColorScheme.fromSeed(seedColor: C.blue),
              textTheme: const TextTheme(
                  headlineSmall:
                      TextStyle(fontWeight: FontWeight.w900, color: C.navy),
                  titleLarge:
                      TextStyle(fontWeight: FontWeight.w800, color: C.navy)),
              inputDecorationTheme: InputDecorationTheme(
                  filled: true,
                  fillColor: Colors.white.withValues(alpha: .7),
                  border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(18),
                      borderSide: BorderSide.none)),
              filledButtonTheme: FilledButtonThemeData(
                  style: FilledButton.styleFrom(
                      minimumSize: const Size.fromHeight(54),
                      shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(18))))),
          routes: {
            '/': (_) => const Splash(),
            '/login': (_) => const Login(),
            '/register': (_) => const Register(),
            '/forgot': (_) => const Forgot(),
            '/home': (_) => const Home(),
            '/assessment': (_) => const Assessment(),
            '/history': (_) => const History(),
            '/profile': (_) => const Profile(),
            '/password': (_) => const Password(),
            '/about': (_) => const About()
          });
}

class Bg extends StatelessWidget {
  const Bg(this.child, {super.key});
  final Widget child;
  @override
  Widget build(c) => DecoratedBox(
      decoration: const BoxDecoration(
          gradient: LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: [
            Color(0xfff8fcff),
            Color(0xffe5efff),
            Color(0xffe9fbf7)
          ])),
      child: Stack(children: [
        Positioned(top: -100, right: -80, child: orb(C.cyan)),
        Positioned(bottom: -130, left: -90, child: orb(C.blue)),
        SafeArea(child: child)
      ]));
  static Widget orb(Color c) => Container(
      width: 280,
      height: 280,
      decoration: BoxDecoration(
          shape: BoxShape.circle, color: c.withValues(alpha: .14)));
}

class Glass extends StatelessWidget {
  const Glass(this.child, {this.pad = const EdgeInsets.all(20), super.key});
  final Widget child;
  final EdgeInsets pad;
  @override
  Widget build(c) => ClipRRect(
      borderRadius: BorderRadius.circular(26),
      child: BackdropFilter(
          filter: ImageFilter.blur(sigmaX: 18, sigmaY: 18),
          child: Container(
              padding: pad,
              decoration: BoxDecoration(
                  color: Colors.white.withValues(alpha: .68),
                  borderRadius: BorderRadius.circular(26),
                  border: Border.all(color: Colors.white),
                  boxShadow: const [
                    BoxShadow(
                        color: Color(0x15102a43),
                        blurRadius: 30,
                        offset: Offset(0, 14))
                  ]),
              child: child)));
}

class Brand extends StatelessWidget {
  const Brand({this.big = false, super.key});
  final bool big;
  @override
  Widget build(c) => Row(mainAxisSize: MainAxisSize.min, children: [
        Container(
            width: big ? 62 : 44,
            height: big ? 62 : 44,
            decoration: BoxDecoration(
                gradient: const LinearGradient(colors: [C.blue, C.cyan]),
                borderRadius: BorderRadius.circular(18)),
            child: Icon(Icons.health_and_safety_rounded,
                color: Colors.white, size: big ? 35 : 25)),
        const SizedBox(width: 12),
        Text('CerviXAI',
            style: TextStyle(
                fontSize: big ? 31 : 23,
                fontWeight: FontWeight.w900,
                color: C.navy))
      ]);
}

class Page extends StatelessWidget {
  const Page(this.title, this.child, {this.actions = const [], super.key});
  final String title;
  final Widget child;
  final List<Widget> actions;
  @override
  Widget build(c) => Scaffold(
          body: Bg(Column(children: [
        Padding(
            padding: const EdgeInsets.all(10),
            child: Row(children: [
              IconButton.filledTonal(
                  onPressed: () => Navigator.pop(c),
                  icon: const Icon(Icons.arrow_back)),
              const SizedBox(width: 8),
              Expanded(
                  child: Text(title, style: Theme.of(c).textTheme.titleLarge)),
              ...actions
            ])),
        Expanded(child: child)
      ])));
}

Widget field(TextEditingController x, String label, IconData icon,
        {bool secret = false, TextInputType? type}) =>
    TextField(
        controller: x,
        obscureText: secret,
        keyboardType: type,
        decoration: InputDecoration(labelText: label, prefixIcon: Icon(icon)));
Widget section(BuildContext c, String title, IconData icon, Widget child) =>
    Glass(Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Row(children: [
        Icon(icon, color: C.blue),
        const SizedBox(width: 10),
        Expanded(child: Text(title, style: Theme.of(c).textTheme.titleLarge))
      ]),
      const SizedBox(height: 15),
      child
    ]));

class Splash extends StatefulWidget {
  const Splash({super.key});
  @override
  State<Splash> createState() => _Splash();
}

class _Splash extends State<Splash> {
  @override
  void initState() {
    super.initState();
    Future.delayed(const Duration(seconds: 2), () {
      if (mounted) Navigator.pushReplacementNamed(context, '/login');
    });
  }

  @override
  Widget build(c) => Scaffold(
      body: Bg(Center(
          child: Padding(
              padding: const EdgeInsets.all(28),
              child: Glass(Column(mainAxisSize: MainAxisSize.min, children: [
                const Brand(big: true),
                const SizedBox(height: 24),
                Text('Clarity behind every prediction',
                    textAlign: TextAlign.center,
                    style: Theme.of(c).textTheme.headlineSmall),
                const SizedBox(height: 9),
                const Text(
                    'Explainable cervical cancer risk assessment for informed clinical decisions.',
                    textAlign: TextAlign.center,
                    style: TextStyle(color: C.muted, height: 1.5)),
                const SizedBox(height: 25),
                const LinearProgressIndicator()
              ]))))));
}

class Login extends StatefulWidget {
  const Login({super.key});
  @override
  State<Login> createState() => _Login();
}

class _Login extends State<Login> {
  final u = TextEditingController(), p = TextEditingController();
  String? error;
  void go() {
    if (u.text.trim().isEmpty || p.text.isEmpty) {
      setState(() => error = 'Enter your username and password.');
      return;
    }
    if (S.i.user.isNotEmpty &&
        (S.i.user != u.text.trim() || S.i.pass != p.text)) {
      setState(() => error = 'Incorrect username or password.');
      return;
    }
    if (S.i.user.isEmpty) S.i.name = u.text.trim();
    Navigator.pushNamedAndRemoveUntil(context, '/home', (_) => false);
  }

  @override
  Widget build(c) => Scaffold(
          body: Bg(ListView(padding: const EdgeInsets.all(24), children: [
        const SizedBox(height: 18),
        const Center(child: Brand(big: true)),
        const SizedBox(height: 30),
        Glass(Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text('Welcome back', style: Theme.of(c).textTheme.headlineSmall),
          const Text('Secure access for healthcare professionals',
              style: TextStyle(color: C.muted)),
          const SizedBox(height: 22),
          field(u, 'Username', Icons.person_outline),
          const SizedBox(height: 12),
          field(p, 'Password', Icons.lock_outline, secret: true),
          if (error != null)
            Padding(
                padding: const EdgeInsets.only(top: 10),
                child: Text(error!, style: const TextStyle(color: C.red))),
          Align(
              alignment: Alignment.centerRight,
              child: TextButton(
                  onPressed: () => Navigator.pushNamed(c, '/forgot'),
                  child: const Text('Forgot password?'))),
          FilledButton(onPressed: go, child: const Text('SIGN IN')),
          Center(
              child: TextButton(
                  onPressed: () => Navigator.pushNamed(c, '/register'),
                  child: const Text('Create a professional account')))
        ]))
      ])));
}

class Register extends StatefulWidget {
  const Register({super.key});
  @override
  State<Register> createState() => _Register();
}

class _Register extends State<Register> {
  final n = TextEditingController(),
      u = TextEditingController(),
      e = TextEditingController(),
      p = TextEditingController(),
      cp = TextEditingController();
  String? error;
  void save() {
    if (n.text.trim().length < 3 ||
        u.text.trim().length < 4 ||
        !e.text.contains('@') ||
        p.text.length < 8 ||
        p.text != cp.text) {
      setState(() => error =
          'Complete all fields. Matching passwords require at least 8 characters.');
      return;
    }
    S.i
      ..name = n.text.trim()
      ..user = u.text.trim()
      ..email = e.text.trim()
      ..pass = p.text;
    ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Account created successfully')));
    Navigator.pop(context);
  }

  @override
  Widget build(c) => Page(
      'Create account',
      ListView(padding: const EdgeInsets.all(20), children: [
        Glass(Column(children: [
          field(n, 'Full name', Icons.badge_outlined),
          const SizedBox(height: 11),
          field(u, 'Username', Icons.person_outline),
          const SizedBox(height: 11),
          field(e, 'Email address', Icons.mail_outline,
              type: TextInputType.emailAddress),
          const SizedBox(height: 11),
          field(p, 'Password', Icons.lock_outline, secret: true),
          const SizedBox(height: 11),
          field(cp, 'Confirm password', Icons.verified_user_outlined,
              secret: true),
          if (error != null)
            Padding(
                padding: const EdgeInsets.all(10),
                child: Text(error!, style: const TextStyle(color: C.red))),
          const SizedBox(height: 16),
          FilledButton(onPressed: save, child: const Text('CREATE ACCOUNT'))
        ]))
      ]));
}

class Forgot extends StatefulWidget {
  const Forgot({super.key});
  @override
  State<Forgot> createState() => _Forgot();
}

class _Forgot extends State<Forgot> {
  final e = TextEditingController();
  bool sent = false;
  @override
  Widget build(c) => Page(
      'Reset password',
      ListView(padding: const EdgeInsets.all(20), children: [
        Glass(Column(children: [
          const Icon(Icons.mark_email_read_outlined, size: 56, color: C.blue),
          const SizedBox(height: 14),
          Text(sent ? 'Check your email' : 'Recover your account',
              style: Theme.of(c).textTheme.titleLarge),
          const SizedBox(height: 9),
          Text(
              sent
                  ? 'If an account exists, a reset link has been requested.'
                  : 'Enter the email associated with your account.',
              textAlign: TextAlign.center,
              style: const TextStyle(color: C.muted)),
          if (!sent) ...[
            const SizedBox(height: 18),
            field(e, 'Email address', Icons.mail_outline,
                type: TextInputType.emailAddress),
            const SizedBox(height: 16),
            FilledButton(
                onPressed: () => setState(() => sent = e.text.contains('@')),
                child: const Text('REQUEST RESET'))
          ]
        ]))
      ]));
}

class Home extends StatelessWidget {
  const Home({super.key});
  @override
  Widget build(c) => Scaffold(
          body: Bg(ListView(padding: const EdgeInsets.all(20), children: [
        Row(children: [
          const Brand(),
          const Spacer(),
          IconButton.filledTonal(
              onPressed: () => Navigator.pushNamed(c, '/profile'),
              icon: const Icon(Icons.person_outline))
        ]),
        const SizedBox(height: 27),
        Text('Good day, ${S.i.name}',
            style: Theme.of(c).textTheme.headlineSmall),
        const Text('What would you like to review today?',
            style: TextStyle(color: C.muted)),
        const SizedBox(height: 20),
        Glass(Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          const Icon(Icons.biotech, size: 42, color: C.blue),
          const SizedBox(height: 14),
          Text('New patient assessment',
              style: Theme.of(c).textTheme.titleLarge),
          const Text(
              'Request an explainable AI risk classification using a patient ID.',
              style: TextStyle(color: C.muted)),
          const SizedBox(height: 18),
          FilledButton.icon(
              onPressed: () => Navigator.pushNamed(c, '/assessment'),
              icon: const Icon(Icons.add),
              label: const Text('START ASSESSMENT'))
        ])),
        const SizedBox(height: 15),
        Row(children: [
          Expanded(child: dash(c, Icons.history, 'History', '/history')),
          const SizedBox(width: 12),
          Expanded(child: dash(c, Icons.info_outline, 'About', '/about'))
        ]),
        const SizedBox(height: 15),
        const Glass(
            Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Icon(Icons.shield_outlined, color: C.blue),
          SizedBox(width: 10),
          Expanded(
              child: Text(
                  'Clinical support only. Interpret results with screening data, examination findings and professional judgement.',
                  style: TextStyle(color: C.muted)))
        ]))
      ])));
  Widget dash(BuildContext c, IconData i, String t, String r) => InkWell(
      onTap: () => Navigator.pushNamed(c, r),
      child:
          Glass(Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Icon(i, color: C.cyan, size: 31),
        const SizedBox(height: 14),
        Text(t, style: const TextStyle(fontWeight: FontWeight.w800)),
        const Icon(Icons.arrow_forward, size: 18, color: C.muted)
      ])));
}

class Assessment extends StatefulWidget {
  const Assessment({super.key});
  @override
  State<Assessment> createState() => _Assessment();
}

class _Assessment extends State<Assessment> {
  final id = TextEditingController();
  bool busy = false;
  String? error;
  Future<void> run() async {
    final n = int.tryParse(id.text.trim());
    if (n == null || n < 0) {
      setState(() => error = 'Enter a valid numeric patient ID.');
      return;
    }
    setState(() {
      busy = true;
      error = null;
    });
    try {
      final r = await http
          .get(Uri.parse('$apiUrl/cancer-report?patient_id=$n'))
          .timeout(const Duration(seconds: 30));
      if (r.statusCode != 200)
        throw Exception('Server returned ${r.statusCode}');
      final x = P.fromJson(jsonDecode(r.body));
      S.i.history.insert(0, H(x.id, x.result, x.risk, DateTime.now()));
      if (mounted)
        Navigator.push(
            context, MaterialPageRoute(builder: (_) => Prediction(x)));
    } catch (e) {
      if (mounted)
        setState(
            () => error = 'Assessment failed. Check backend connection.\n$e');
    } finally {
      if (mounted) setState(() => busy = false);
    }
  }

  @override
  Widget build(c) => Page(
      'Patient assessment',
      ListView(padding: const EdgeInsets.all(20), children: [
        Glass(Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          const Icon(Icons.manage_search, size: 46, color: C.blue),
          const SizedBox(height: 15),
          Text('Find patient record', style: Theme.of(c).textTheme.titleLarge),
          const Text(
              'Enter the dataset patient ID used by the prediction service.',
              style: TextStyle(color: C.muted)),
          const SizedBox(height: 19),
          field(id, 'Patient ID', Icons.tag, type: TextInputType.number),
          if (error != null)
            Padding(
                padding: const EdgeInsets.only(top: 12),
                child: Text(error!, style: const TextStyle(color: C.red))),
          const SizedBox(height: 18),
          FilledButton.icon(
              onPressed: busy ? null : run,
              icon: busy
                  ? const SizedBox.square(
                      dimension: 18,
                      child: CircularProgressIndicator(strokeWidth: 2))
                  : const Icon(Icons.auto_awesome),
              label: Text(busy ? 'ANALYSING...' : 'GENERATE ASSESSMENT'))
        ]))
      ]));
}

class P {
  P(
      this.id,
      this.result,
      this.risk,
      this.safe,
      this.threshold,
      this.biopsy,
      this.biopsyRisk,
      this.hpv,
      this.hpvRisk,
      this.method,
      this.explain,
      this.factors,
      this.interpretation,
      this.next,
      this.note);
  final int id;
  final String result, biopsy, hpv, method, explain, interpretation, next, note;
  final double risk, safe, threshold, biopsyRisk, hpvRisk;
  final List<F> factors;
  factory P.fromJson(Map<String, dynamic> j) {
    final o = j['overall_cancer_prediction'] as Map<String, dynamic>? ?? {},
        s = j['supporting_predictions'] as Map<String, dynamic>? ?? {},
        b = s['biopsy'] as Map<String, dynamic>? ?? {},
        h = s['hpv'] as Map<String, dynamic>? ?? {},
        x = j['xai_explanation'] as Map<String, dynamic>? ?? {};
    double n(v) => (v as num?)?.toDouble() ?? 0;
    final fs = x['top_supporting_factors'] as List? ?? [];
    return P(
        (j['patient_id'] as num?)?.toInt() ?? 0,
        o['prediction']?.toString() ?? 'Unknown',
        n(o['cancer_probability_percent']),
        n(o['no_cancer_probability_percent']),
        n(o['classification_threshold_percent']),
        b['prediction']?.toString() ?? 'Unknown',
        n(b['positive_probability_percent']),
        h['prediction']?.toString() ?? 'Unknown',
        n(h['positive_probability_percent']),
        x['method']?.toString() ?? 'Explainable AI',
        x['explanation']?.toString() ?? '',
        fs.whereType<Map<String, dynamic>>().map(F.fromJson).toList(),
        j['interpretation']?.toString() ?? '',
        j['recommended_next_step']?.toString() ?? '',
        j['important_note']?.toString() ?? '');
  }
}

class F {
  F(this.rank, this.name, this.value, this.result);
  final int rank;
  final String name, value, result;
  factory F.fromJson(Map<String, dynamic> j) => F(
      (j['rank'] as num?)?.toInt() ?? 0,
      j['factor']?.toString() ?? 'Factor',
      j['patient_value']?.toString() ?? '-',
      j['xai_result']?.toString() ?? '');
}

class Prediction extends StatelessWidget {
  const Prediction(this.x, {super.key});
  final P x;
  @override
  Widget build(c) {
    final positive = x.result.toLowerCase().contains('positive'),
        color = positive ? C.red : const Color(0xff159474);
    return Page(
        'Assessment result',
        ListView(padding: const EdgeInsets.all(20), children: [
          Glass(Column(children: [
            Row(children: [
              Text('PATIENT #${x.id}',
                  style: const TextStyle(
                      color: C.muted, fontWeight: FontWeight.bold)),
              const Spacer(),
              Icon(positive ? Icons.warning_amber : Icons.verified,
                  color: color)
            ]),
            const SizedBox(height: 15),
            Text(x.result,
                textAlign: TextAlign.center,
                style: TextStyle(
                    fontSize: 27, fontWeight: FontWeight.w900, color: color)),
            const SizedBox(height: 16),
            Row(children: [
              Expanded(child: metric('Cancer', x.risk, color)),
              const SizedBox(width: 10),
              Expanded(child: metric('No cancer', x.safe, C.cyan))
            ]),
            const SizedBox(height: 9),
            Text('Classification threshold: ${x.threshold.toStringAsFixed(1)}%',
                style: const TextStyle(color: C.muted))
          ])),
          const SizedBox(height: 14),
          section(
              c,
              'Supporting models',
              Icons.hub_outlined,
              Column(children: [
                support('Biopsy', x.biopsy, x.biopsyRisk),
                const Divider(height: 24),
                support('HPV', x.hpv, x.hpvRisk)
              ])),
          const SizedBox(height: 14),
          section(
              c,
              '${x.method} explanation',
              Icons.auto_awesome_outlined,
              Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text(x.explain),
                const SizedBox(height: 12),
                ...x.factors.map((f) => Container(
                    width: double.infinity,
                    margin: const EdgeInsets.only(bottom: 9),
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                        color: C.blue.withValues(alpha: .06),
                        borderRadius: BorderRadius.circular(14)),
                    child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text('${f.rank}. ${f.name}',
                              style:
                                  const TextStyle(fontWeight: FontWeight.bold)),
                          Text('Patient value: ${f.value}',
                              style: const TextStyle(color: C.muted)),
                          Text(f.result)
                        ])))
              ])),
          const SizedBox(height: 14),
          section(c, 'Clinical interpretation', Icons.fact_check_outlined,
              Text(x.interpretation)),
          const SizedBox(height: 14),
          section(c, 'Recommended next step', Icons.arrow_circle_right_outlined,
              Text(x.next)),
          const SizedBox(height: 14),
          section(c, 'Important clinical note', Icons.shield_outlined,
              Text(x.note, style: const TextStyle(color: C.muted)))
        ]));
  }

  Widget metric(String l, double v, Color c) => Container(
      padding: const EdgeInsets.all(13),
      decoration: BoxDecoration(
          color: c.withValues(alpha: .1),
          borderRadius: BorderRadius.circular(16)),
      child: Column(children: [
        Text('${v.toStringAsFixed(1)}%',
            style:
                TextStyle(fontSize: 21, fontWeight: FontWeight.w900, color: c)),
        Text(l)
      ]));
  Widget support(String l, String p, double v) => Row(children: [
        Expanded(
            child:
                Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(l, style: const TextStyle(fontWeight: FontWeight.bold)),
          Text(p, style: const TextStyle(color: C.muted))
        ])),
        Text('${v.toStringAsFixed(1)}%',
            style: const TextStyle(
                fontSize: 18, fontWeight: FontWeight.bold, color: C.blue))
      ]);
}

class History extends StatefulWidget {
  const History({super.key});
  @override
  State<History> createState() => _History();
}

class _History extends State<History> {
  @override
  Widget build(c) {
    final h = S.i.history;
    return Page(
        'Prediction history',
        h.isEmpty
            ? const Center(
                child: Column(mainAxisSize: MainAxisSize.min, children: [
                Icon(Icons.history, size: 55, color: C.muted),
                SizedBox(height: 10),
                Text('No assessments yet', style: TextStyle(color: C.muted))
              ]))
            : ListView.separated(
                padding: const EdgeInsets.all(20),
                itemCount: h.length,
                separatorBuilder: (_, __) => const SizedBox(height: 10),
                itemBuilder: (_, i) {
                  final x = h[i],
                      positive = x.result.toLowerCase().contains('positive'),
                      color = positive ? C.red : const Color(0xff159474);
                  return Glass(Row(children: [
                    CircleAvatar(
                        backgroundColor: color.withValues(alpha: .12),
                        child: Icon(
                            positive ? Icons.warning_amber : Icons.check,
                            color: color)),
                    const SizedBox(width: 12),
                    Expanded(
                        child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                          Text('Patient #${x.id}',
                              style:
                                  const TextStyle(fontWeight: FontWeight.bold)),
                          Text(x.result,
                              style: const TextStyle(color: C.muted)),
                          Text('${x.date.day}/${x.date.month}/${x.date.year}',
                              style:
                                  const TextStyle(fontSize: 12, color: C.muted))
                        ])),
                    Text('${x.risk.toStringAsFixed(1)}%',
                        style: const TextStyle(fontWeight: FontWeight.bold))
                  ]));
                }),
        actions: [
          if (h.isNotEmpty)
            IconButton(
                onPressed: () => setState(h.clear),
                icon: const Icon(Icons.delete_outline))
        ]);
  }
}

class Profile extends StatelessWidget {
  const Profile({super.key});
  @override
  Widget build(c) => Page(
      'My profile',
      ListView(padding: const EdgeInsets.all(20), children: [
        Glass(Column(children: [
          const CircleAvatar(
              radius: 39,
              backgroundColor: Color(0xffe5eeff),
              child: Icon(Icons.person, size: 43, color: C.blue)),
          const SizedBox(height: 12),
          Text(S.i.name,
              textAlign: TextAlign.center,
              style: Theme.of(c).textTheme.titleLarge),
          Text(S.i.email.isEmpty ? 'Healthcare professional' : S.i.email,
              style: const TextStyle(color: C.muted))
        ])),
        const SizedBox(height: 14),
        Glass(Column(children: [
          ListTile(
              leading: const Icon(Icons.lock_outline),
              title: const Text('Change password'),
              trailing: const Icon(Icons.chevron_right),
              onTap: () => Navigator.pushNamed(c, '/password')),
          const Divider(height: 1),
          ListTile(
              leading: const Icon(Icons.info_outline),
              title: const Text('About CerviXAI'),
              trailing: const Icon(Icons.chevron_right),
              onTap: () => Navigator.pushNamed(c, '/about'))
        ])),
        const SizedBox(height: 14),
        OutlinedButton.icon(
            onPressed: () =>
                Navigator.pushNamedAndRemoveUntil(c, '/login', (_) => false),
            icon: const Icon(Icons.logout),
            label: const Text('SIGN OUT'))
      ]));
}

class Password extends StatefulWidget {
  const Password({super.key});
  @override
  State<Password> createState() => _Password();
}

class _Password extends State<Password> {
  final old = TextEditingController(),
      next = TextEditingController(),
      confirm = TextEditingController();
  String? msg;
  bool ok = false;
  void save() {
    if (S.i.pass.isNotEmpty && old.text != S.i.pass) {
      setState(() {
        ok = false;
        msg = 'Current password is incorrect.';
      });
      return;
    }
    if (next.text.length < 8 || next.text != confirm.text) {
      setState(() {
        ok = false;
        msg = 'New passwords must match and contain 8+ characters.';
      });
      return;
    }
    S.i.pass = next.text;
    setState(() {
      ok = true;
      msg = 'Password updated successfully.';
    });
  }

  @override
  Widget build(c) => Page(
      'Change password',
      ListView(padding: const EdgeInsets.all(20), children: [
        Glass(Column(children: [
          field(old, 'Current password', Icons.lock_outline, secret: true),
          const SizedBox(height: 11),
          field(next, 'New password', Icons.password, secret: true),
          const SizedBox(height: 11),
          field(confirm, 'Confirm new password', Icons.verified_user_outlined,
              secret: true),
          if (msg != null)
            Padding(
                padding: const EdgeInsets.all(11),
                child: Text(msg!,
                    style: TextStyle(
                        color: ok ? const Color(0xff159474) : C.red,
                        fontWeight: FontWeight.bold))),
          const SizedBox(height: 15),
          FilledButton(onPressed: save, child: const Text('UPDATE PASSWORD'))
        ]))
      ]));
}

class About extends StatelessWidget {
  const About({super.key});
  @override
  Widget build(c) => Page(
      'About CerviXAI',
      ListView(padding: const EdgeInsets.all(20), children: [
        Glass(Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          const Brand(big: true),
          const SizedBox(height: 20),
          Text('Explainable intelligence for clinical support',
              style: Theme.of(c).textTheme.headlineSmall),
          const SizedBox(height: 10),
          const Text(
              'CerviXAI combines machine-learning predictions with human-readable explanations to support cervical cancer risk assessment. It is designed for healthcare professionals and does not replace clinical judgement.')
        ])),
        const SizedBox(height: 14),
        section(
            c,
            'Core capabilities',
            Icons.stars_outlined,
            const Column(children: [
              Feature(Icons.biotech_outlined, 'AI-assisted patient assessment'),
              Feature(Icons.psychology_alt_outlined,
                  'Explainable supporting factors'),
              Feature(Icons.history, 'Assessment history'),
              Feature(Icons.security, 'Professional access workflow')
            ])),
        const SizedBox(height: 14),
        const Center(
            child: Text('Version 1.0.0 - Flutter edition',
                style: TextStyle(color: C.muted)))
      ]));
}

class Feature extends StatelessWidget {
  const Feature(this.icon, this.text, {super.key});
  final IconData icon;
  final String text;
  @override
  Widget build(c) => Padding(
      padding: const EdgeInsets.symmetric(vertical: 7),
      child: Row(children: [
        Icon(icon, color: C.cyan),
        const SizedBox(width: 11),
        Expanded(child: Text(text))
      ]));
}

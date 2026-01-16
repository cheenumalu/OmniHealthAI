import 'dart:math';
import 'dart:ui';
import 'package:flutter/material.dart';

void main() {
  runApp(const OmniHealthApp());
}

class OmniHealthApp extends StatelessWidget {
  const OmniHealthApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "OmniHealth AI",
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark(useMaterial3: true),
      home: const OmniHealthHome(),
    );
  }
}

class OmniHealthHome extends StatefulWidget {
  const OmniHealthHome({super.key});

  @override
  State<OmniHealthHome> createState() => _OmniHealthHomeState();
}

class _OmniHealthHomeState extends State<OmniHealthHome>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;

  // Raw cursor from pointer events
  Offset _cursorTarget = const Offset(-9999, -9999);

  // Smoothed cursor (inertia)
  Offset _cursorSmooth = const Offset(-9999, -9999);

  final TextEditingController _inputCtrl = TextEditingController();
  String _lang = "English";
  String _report = "Ready for analysis ✅";
  String _status = "Idle";

  @override
  void initState() {
    super.initState();

    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 6),
    )..repeat();

    // ✅ Cursor inertia update loop
    _controller.addListener(_tickInertia);
  }

  void _tickInertia() {
    // if cursor not active
    if (_cursorTarget.dx < 0 || _cursorTarget.dy < 0) {
      if (_cursorSmooth.dx > 0 && _cursorSmooth.dy > 0) {
        setState(() {
          _cursorSmooth = const Offset(-9999, -9999);
        });
      }
      return;
    }

    // ✅ Smooth follow with inertia (lerp factor)
    const double lerpFactor = 0.18; // smaller -> more smooth delay
    final next = Offset(
      lerpDouble(_cursorSmooth.dx, _cursorTarget.dx, lerpFactor)!,
      lerpDouble(_cursorSmooth.dy, _cursorTarget.dy, lerpFactor)!,
    );

    // update only if moved (avoid extra rebuilds)
    if ((next - _cursorSmooth).distance > 0.1) {
      setState(() => _cursorSmooth = next);
    }
  }

  @override
  void dispose() {
    _controller.removeListener(_tickInertia);
    _controller.dispose();
    _inputCtrl.dispose();
    super.dispose();
  }

  void runAnalysis() async {
    setState(() {
      _status = "Consulting Medical Engine... ⏳";
      _report = "Generating report...\n\n(Connect this UI to Gemini backend later)";
    });

    await Future.delayed(const Duration(milliseconds: 900));

    setState(() {
      _status = "Report generated ✅";
      _report = """CONFIDENCE SCORE: 90%

INFO:
- Category: Medical guidance UI demo

PERSONALIZED ADVICE:
- Calm medical theme + pulsing ECG + cursor inertia glow.

FIRST AID:
Do:
1) Hydrate
2) Rest
3) Monitor symptoms
Don't:
1) Panic
2) Overmedicate
3) Ignore warning signs

SOURCE:
Search: "WHO symptom guidance"

SAFETY:
This output is demo only.

Language: $_lang
Input: ${_inputCtrl.text.trim().isEmpty ? "(none)" : _inputCtrl.text.trim()}
""";
    });
  }

  void clear() {
    setState(() {
      _status = "Cleared 🗑️";
      _report = "Ready for analysis ✅";
      _inputCtrl.clear();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Listener(
        // ✅ cursor follows even while click & drag
        onPointerDown: (e) => _cursorTarget = e.position,
        onPointerMove: (e) => _cursorTarget = e.position,
        onPointerHover: (e) => _cursorTarget = e.position,
        onPointerUp: (e) => _cursorTarget = e.position,
        child: MouseRegion(
          onExit: (_) => setState(() {
            _cursorTarget = const Offset(-9999, -9999);
            _cursorSmooth = const Offset(-9999, -9999);
          }),
          child: AnimatedBuilder(
            animation: _controller,
            builder: (context, _) {
              final t = _controller.value;

              return Stack(
                children: [
                  // Aurora background
                  Positioned.fill(
                    child: CustomPaint(
                      painter: AuroraPainter(t: t),
                    ),
                  ),

                  // ✅ ECG background - more visible
                  Positioned.fill(
                    child: Opacity(
                      opacity: 0.35, // ✅ increased
                      child: CustomPaint(
                        painter: ECGPainter(t: t),
                      ),
                    ),
                  ),

                  // ✅ Cursor glow with inertia
                  Positioned.fill(
                    child: IgnorePointer(
                      child: CustomPaint(
                        painter: CursorGlowPainter(cursor: _cursorSmooth),
                      ),
                    ),
                  ),

                  // UI content
                  SafeArea(
                    child: Center(
                      child: Padding(
                        padding: const EdgeInsets.fromLTRB(18, 28, 18, 30),
                        child: ConstrainedBox(
                          constraints: const BoxConstraints(maxWidth: 980),
                          child: GlassPanel(
                            child: Padding(
                              padding: const EdgeInsets.all(22),
                              child: Column(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  // Header
                                  Row(
                                    mainAxisAlignment:
                                        MainAxisAlignment.spaceBetween,
                                    children: [
                                      Column(
                                        crossAxisAlignment:
                                            CrossAxisAlignment.start,
                                        children: const [
                                          Text(
                                            "⚕️ OmniHealth AI",
                                            style: TextStyle(
                                              fontSize: 22,
                                              fontWeight: FontWeight.w700,
                                              letterSpacing: 0.2,
                                            ),
                                          ),
                                          SizedBox(height: 4),
                                          Text(
                                            "Aurora medical UI • PULSING ECG • cursor inertia glow",
                                            style: TextStyle(
                                              fontSize: 13,
                                              color: Colors.white70,
                                            ),
                                          ),
                                        ],
                                      ),
                                      Container(
                                        padding: const EdgeInsets.symmetric(
                                            horizontal: 12, vertical: 8),
                                        decoration: BoxDecoration(
                                          borderRadius:
                                              BorderRadius.circular(100),
                                          border: Border.all(
                                              color: Colors.white
                                                  .withOpacity(.18)),
                                          color: Colors.white.withOpacity(.06),
                                        ),
                                        child: const Text(
                                          "🧬 Health Engine • Live UI",
                                          style: TextStyle(fontSize: 12),
                                        ),
                                      )
                                    ],
                                  ),
                                  const SizedBox(height: 16),

                                  // Body grid
                                  LayoutBuilder(builder: (context, c) {
                                    final isMobile = c.maxWidth < 850;

                                    return isMobile
                                        ? Column(
                                            children: [
                                              _inputCard(),
                                              const SizedBox(height: 14),
                                              _reportCard(),
                                            ],
                                          )
                                        : Row(
                                            crossAxisAlignment:
                                                CrossAxisAlignment.start,
                                            children: [
                                              Expanded(
                                                  flex: 11,
                                                  child: _inputCard()),
                                              const SizedBox(width: 14),
                                              Expanded(
                                                  flex: 9,
                                                  child: _reportCard()),
                                            ],
                                          );
                                  }),

                                  const SizedBox(height: 12),
                                  const Text(
                                    "DISCLAIMER: Educational tool only. Consult a doctor for real medical advice.",
                                    textAlign: TextAlign.center,
                                    style: TextStyle(
                                        fontSize: 12, color: Colors.white60),
                                  )
                                ],
                              ),
                            ),
                          ),
                        ),
                      ),
                    ),
                  ),
                ],
              );
            },
          ),
        ),
      ),
    );
  }

  Widget _inputCard() {
    return FrostCard(
      title: "Input",
      child: Column(
        children: [
          Row(
            children: [
              Expanded(
                child: TextField(
                  controller: _inputCtrl,
                  style: const TextStyle(fontSize: 14),
                  decoration: InputDecoration(
                    hintText: "Type medicine / symptom name...",
                    hintStyle: const TextStyle(color: Colors.white54),
                    filled: true,
                    fillColor: Colors.white.withOpacity(.06),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(14),
                      borderSide:
                          BorderSide(color: Colors.white.withOpacity(.18)),
                    ),
                    enabledBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(14),
                      borderSide:
                          BorderSide(color: Colors.white.withOpacity(.18)),
                    ),
                  ),
                ),
              ),
              const SizedBox(width: 10),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10),
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(14),
                  border: Border.all(color: Colors.white.withOpacity(.18)),
                  color: Colors.white.withOpacity(.06),
                ),
                child: DropdownButtonHideUnderline(
                  child: DropdownButton<String>(
                    value: _lang,
                    dropdownColor: const Color(0xFF0A0F16),
                    items: const [
                      DropdownMenuItem(value: "English", child: Text("English")),
                      DropdownMenuItem(value: "Hindi", child: Text("Hindi")),
                      DropdownMenuItem(
                          value: "Spanish", child: Text("Spanish")),
                      DropdownMenuItem(value: "French", child: Text("French")),
                    ],
                    onChanged: (v) => setState(() => _lang = v!),
                  ),
                ),
              )
            ],
          ),
          const SizedBox(height: 12),
          Row(
            children: [
              ElevatedButton(
                onPressed: runAnalysis,
                style: ElevatedButton.styleFrom(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                  backgroundColor: const Color(0xFF1EFFF0).withOpacity(.12),
                  foregroundColor: Colors.white,
                  side: BorderSide(
                    color: const Color(0xFF1EFFF0).withOpacity(.25),
                  ),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(14),
                  ),
                ),
                child: const Text("Run Advanced Analysis 🔍"),
              ),
              const SizedBox(width: 10),
              OutlinedButton(
                onPressed: clear,
                style: OutlinedButton.styleFrom(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                  side: BorderSide(color: Colors.white.withOpacity(.18)),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(14),
                  ),
                ),
                child: const Text("Clear"),
              ),
            ],
          ),
          const SizedBox(height: 10),
          const Align(
            alignment: Alignment.centerLeft,
            child: Text(
              "UI demo. Connect to Streamlit/Gemini backend later.",
              style: TextStyle(fontSize: 12, color: Colors.white60),
            ),
          ),
        ],
      ),
    );
  }

  Widget _reportCard() {
    return FrostCard(
      title: "Personalized Report",
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            _report,
            style: const TextStyle(fontSize: 14, height: 1.45),
          ),
          const SizedBox(height: 8),
          Text(
            _status,
            style: const TextStyle(fontSize: 12, color: Colors.white70),
          )
        ],
      ),
    );
  }
}

/* --------------------------
   UI Components
--------------------------- */

class GlassPanel extends StatelessWidget {
  final Widget child;
  const GlassPanel({super.key, required this.child});

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(26),
        border: Border.all(color: Colors.white.withOpacity(.18)),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(.55),
            blurRadius: 70,
            offset: const Offset(0, 22),
          ),
        ],
      ),
      child: ClipRRect(
        borderRadius: BorderRadius.circular(26),
        child: BackdropFilter(
          filter: ImageFilter.blur(sigmaX: 14, sigmaY: 14),
          child: Container(
            decoration: BoxDecoration(
              color: const Color(0xFF070A10).withOpacity(.42),
            ),
            child: child,
          ),
        ),
      ),
    );
  }
}

class FrostCard extends StatelessWidget {
  final String title;
  final Widget child;
  const FrostCard({super.key, required this.title, required this.child});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.black.withOpacity(.22),
        borderRadius: BorderRadius.circular(18),
        border: Border.all(color: Colors.white.withOpacity(.14)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title,
              style:
                  const TextStyle(fontSize: 14, fontWeight: FontWeight.w600)),
          const SizedBox(height: 10),
          child,
        ],
      ),
    );
  }
}

/* --------------------------
   Background Painters
--------------------------- */

class AuroraPainter extends CustomPainter {
  final double t;
  AuroraPainter({required this.t});

  @override
  void paint(Canvas canvas, Size size) {
    final rect = Offset.zero & size;

    // base gradient
    final bg = Paint()
      ..shader = RadialGradient(
        center: Alignment(-0.7 + 0.1 * sin(t * 2 * pi), -0.6),
        radius: 1.3,
        colors: const [
          Color(0xFF0B1020),
          Color(0xFF06070B),
        ],
      ).createShader(rect);

    canvas.drawRect(rect, bg);

    void blob(Offset center, double radius, List<Color> colors) {
      final p = Paint()
        ..shader = RadialGradient(colors: colors)
            .createShader(Rect.fromCircle(center: center, radius: radius));
      canvas.drawCircle(center, radius, p);
    }

    blob(
      Offset(size.width * (0.25 + 0.04 * sin(t * 2 * pi)),
          size.height * (0.22 + 0.05 * cos(t * 2 * pi))),
      size.width * 0.55,
      [const Color(0xFF1EFFF0).withOpacity(0.18), Colors.transparent],
    );

    blob(
      Offset(size.width * (0.78 + 0.04 * cos(t * 2 * pi)),
          size.height * (0.32 + 0.04 * sin(t * 2 * pi))),
      size.width * 0.50,
      [const Color(0xFF7AA7FF).withOpacity(0.16), Colors.transparent],
    );

    blob(
      Offset(size.width * 0.5, size.height * (0.82 + 0.03 * sin(t * 2 * pi))),
      size.width * 0.55,
      [const Color(0xFFFF8AD6).withOpacity(0.07), Colors.transparent],
    );
  }

  @override
  bool shouldRepaint(covariant AuroraPainter oldDelegate) => oldDelegate.t != t;
}

class ECGPainter extends CustomPainter {
  final double t;
  ECGPainter({required this.t});

  @override
  void paint(Canvas canvas, Size size) {
    final baseY = size.height * 0.66;

    // ✅ pulsing factor like heartbeat
    // peaks every cycle and fades smoothly
    final pulse = (sin(t * 2 * pi * 1.35) + 1) / 2; // 0..1
    final glowStrength = 0.35 + (pulse * 0.35); // 0.35..0.70

    final paint = Paint()
      ..color = const Color(0xFF1EFFF0).withOpacity(glowStrength)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2.6
      ..strokeCap = StrokeCap.round
      ..strokeJoin = StrokeJoin.round
      ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 3);

    final faintLine = Paint()
      ..color = Colors.white.withOpacity(0.06)
      ..strokeWidth = 1;

    canvas.drawLine(Offset(0, baseY), Offset(size.width, baseY), faintLine);

    final path = Path();

    final speed = size.width * 0.22;
    final phase = (t * speed) % size.width;

    double x = -size.width;
    path.moveTo(x, baseY);

    while (x < size.width * 2) {
      final start = x - phase;

      // flat
      path.lineTo(start + 0, baseY);
      path.lineTo(start + 55, baseY);

      // small bump
      path.lineTo(start + 72, baseY - 12);
      path.lineTo(start + 84, baseY);

      // big spike
      path.lineTo(start + 100, baseY);
      path.lineTo(start + 112, baseY - 58);
      path.lineTo(start + 130, baseY + 34);
      path.lineTo(start + 152, baseY);

      // recovery
      path.lineTo(start + 190, baseY);
      path.lineTo(start + 220, baseY);

      x += 260;
    }

    canvas.drawPath(path, paint);

    // ✅ Secondary glow layer (extra pulse highlight)
    final glow = Paint()
      ..color = const Color(0xFF7AA7FF).withOpacity(0.10 + pulse * 0.10)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 4.0
      ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 8);

    canvas.drawPath(path, glow);
  }

  @override
  bool shouldRepaint(covariant ECGPainter oldDelegate) => oldDelegate.t != t;
}

class CursorGlowPainter extends CustomPainter {
  final Offset cursor;
  CursorGlowPainter({required this.cursor});

  @override
  void paint(Canvas canvas, Size size) {
    if (cursor.dx < 0 || cursor.dy < 0) return;

    // ✅ Bigger spread, lower brightness
    const double bigRadius = 320;
    const double midRadius = 160;
    const double coreRadius = 55;

    final glow = Paint()
      ..shader = RadialGradient(
        colors: [
          const Color(0xFF1EFFF0).withOpacity(0.08), // ✅ lower
          const Color(0xFF7AA7FF).withOpacity(0.05),
          Colors.transparent,
        ],
        stops: const [0.0, 0.45, 1.0],
      ).createShader(Rect.fromCircle(center: cursor, radius: bigRadius));

    canvas.drawCircle(cursor, bigRadius, glow);

    final midGlow = Paint()
      ..shader = RadialGradient(
        colors: [
          Colors.white.withOpacity(0.05),
          Colors.transparent,
        ],
        stops: const [0.0, 1.0],
      ).createShader(Rect.fromCircle(center: cursor, radius: midRadius));

    canvas.drawCircle(cursor, midRadius, midGlow);

    final core = Paint()
      ..shader = RadialGradient(
        colors: [
          Colors.white.withOpacity(0.10),
          Colors.transparent,
        ],
        stops: const [0.0, 1.0],
      ).createShader(Rect.fromCircle(center: cursor, radius: coreRadius));

    canvas.drawCircle(cursor, coreRadius, core);
  }

  @override
  bool shouldRepaint(covariant CursorGlowPainter oldDelegate) =>
      oldDelegate.cursor != cursor;
}

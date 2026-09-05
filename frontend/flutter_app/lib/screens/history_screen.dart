import 'package:flutter/material.dart';

import '../models.dart';
import '../services/api_service.dart';
import '../session.dart';
import '../theme.dart';
import '../widgets/common.dart';

class HistoryScreen extends StatefulWidget {
  const HistoryScreen({super.key});
  @override
  State<HistoryScreen> createState() => _HistoryScreenState();
}

class _HistoryScreenState extends State<HistoryScreen> {
  late Future<List<HistoryEntry>> _future;
  late int _seenHistoryVersion;

  @override
  void initState() {
    super.initState();
    _future = Session.i.api.fetchHistory();
    _seenHistoryVersion = Session.i.historyVersion;
    Session.i.addListener(_onSessionChanged);
  }

  @override
  void dispose() {
    Session.i.removeListener(_onSessionChanged);
    super.dispose();
  }

  // Auto-refresh as soon as a new assessment/screening is saved elsewhere in
  // the app, so this tab is already up to date instead of waiting for a
  // manual pull-to-refresh.
  void _onSessionChanged() {
    if (Session.i.historyVersion != _seenHistoryVersion) {
      _seenHistoryVersion = Session.i.historyVersion;
      _reload();
    }
  }

  Future<void> _reload() async {
    final f = Session.i.api.fetchHistory();
    setState(() {
      _future = f;
    });
    await f;
  }

  Future<void> _clearAll() async {
    try {
      await Session.i.api.clearHistory();
      await _reload();
    } on ApiException catch (e) {
      if (mounted) showSnack(context, e.message);
    }
  }

  Future<void> _deleteOne(int id) async {
    try {
      await Session.i.api.deleteHistoryEntry(id);
      await _reload();
    } on ApiException catch (e) {
      if (mounted) showSnack(context, e.message);
    }
  }

  @override
  Widget build(BuildContext context) => Bg(SafeArea(
        child: Column(children: [
          Padding(
            padding: const EdgeInsets.fromLTRB(20, 12, 12, 4),
            child: Row(children: [
              Expanded(child: Text('Assessment history', style: Theme.of(context).textTheme.titleLarge)),
              FutureBuilder<List<HistoryEntry>>(
                future: _future,
                builder: (context, snap) {
                  final hasEntries = (snap.data?.isNotEmpty ?? false);
                  return IconButton(
                    onPressed: hasEntries ? _clearAll : null,
                    icon: const Icon(Icons.delete_outline_rounded),
                    tooltip: 'Clear history',
                  );
                },
              ),
            ]),
          ),
          Expanded(
            child: RefreshIndicator(
              onRefresh: _reload,
              child: FutureBuilder<List<HistoryEntry>>(
                future: _future,
                builder: (context, snap) {
                  if (snap.connectionState == ConnectionState.waiting) {
                    return const Center(child: CircularProgressIndicator());
                  }
                  if (snap.hasError) {
                    return ListView(children: [
                      const SizedBox(height: 60),
                      EmptyState(icon: Icons.wifi_off_rounded, text: snap.error.toString()),
                    ]);
                  }
                  final items = snap.data ?? [];
                  if (items.isEmpty) {
                    return ListView(children: const [
                      SizedBox(height: 60),
                      EmptyState(icon: Icons.history_rounded, text: 'No assessments yet'),
                    ]);
                  }
                  return ListView.separated(
                    padding: const EdgeInsets.fromLTRB(20, 4, 20, 20),
                    itemCount: items.length,
                    separatorBuilder: (_, __) => const SizedBox(height: 10),
                    itemBuilder: (context, i) {
                      final entry = items[i];
                      final color = entry.isPositive ? AppColors.red : AppColors.success;
                      return Dismissible(
                        key: ValueKey(entry.id),
                        direction: DismissDirection.endToStart,
                        onDismissed: (_) => _deleteOne(entry.id),
                        background: Container(
                          alignment: Alignment.centerRight,
                          padding: const EdgeInsets.only(right: 20),
                          decoration: BoxDecoration(
                              color: AppColors.red.withValues(alpha: .15),
                              borderRadius: BorderRadius.circular(22)),
                          child: const Icon(Icons.delete_outline_rounded, color: AppColors.red),
                        ),
                        child: Glass(Row(children: [
                          CircleAvatar(
                            backgroundColor: color.withValues(alpha: .12),
                            child: Icon(
                              entry.isImage
                                  ? Icons.image_search_rounded
                                  : (entry.isPositive ? Icons.warning_amber_rounded : Icons.check_rounded),
                              color: color,
                            ),
                          ),
                          const SizedBox(width: 12),
                          Expanded(
                            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                              Text(entry.title, style: const TextStyle(fontWeight: FontWeight.bold)),
                              Text(entry.result, style: const TextStyle(color: AppColors.muted)),
                              Text(_formatDate(entry.createdAt),
                                  style: const TextStyle(fontSize: 12, color: AppColors.muted)),
                            ]),
                          ),
                          if (entry.riskPercent != null)
                            Text('${entry.riskPercent!.toStringAsFixed(1)}%',
                                style: const TextStyle(fontWeight: FontWeight.bold)),
                        ])),
                      );
                    },
                  );
                },
              ),
            ),
          ),
        ]),
      ));

  String _formatDate(DateTime d) {
    final local = d.toLocal();
    String two(int n) => n.toString().padLeft(2, '0');
    return '${two(local.day)}/${two(local.month)}/${local.year} · ${two(local.hour)}:${two(local.minute)}';
  }
}

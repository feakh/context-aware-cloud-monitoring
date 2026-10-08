"""Transparent contextual rules. Thresholds are demo choices, not validated SLAs."""
import json
from pathlib import Path

def load_rules():
    return json.loads((Path(__file__).resolve().parents[1] / 'config' / 'rules.json').read_text())

def contextual_conditions(t, r):
    return {
        'cpu_high': t['cpu_percent'] >= r['cpu_high'],
        'memory_high': t['memory_percent'] >= r['memory_high'],
        'disk_high': t['disk_percent'] >= r['disk_high'],
        'service_down': not t['service_available'],
        'response_slow': t['response_ms'] >= r['response_slow_ms'],
        'errors_repeated': t['application_errors'] >= r['errors_repeated'],
    }

def detect_and_classify(t, r):
    c = contextual_conditions(t, r)
    evidence = []
    descriptions = {
        'cpu_high': f"CPU {t['cpu_percent']}% meets threshold {r['cpu_high']}%",
        'memory_high': f"Memory {t['memory_percent']}% meets threshold {r['memory_high']}%",
        'disk_high': f"Disk {t['disk_percent']}% meets threshold {r['disk_high']}%",
        'service_down': 'Service availability is false',
        'response_slow': f"Response {t['response_ms']} ms meets threshold {r['response_slow_ms']} ms",
        'errors_repeated': f"Application errors {t['application_errors']} meet threshold {r['errors_repeated']}",
    }
    evidence = [descriptions[k] for k, active in c.items() if active]
    if c['service_down']:
        priority, rule = 'High', 'H1 Service unavailable'
    elif c['cpu_high'] and c['response_slow'] and c['errors_repeated']:
        priority, rule = 'High', 'H2 High CPU with slow response and repeated errors'
    elif (c['cpu_high'] and c['memory_high']) or c['response_slow'] or c['errors_repeated']:
        priority, rule = 'Medium', 'M1 Combined resource pressure or service degradation'
    elif c['cpu_high'] or c['memory_high'] or c['disk_high']:
        priority, rule = 'Low', 'L1 Isolated resource threshold'
    else:
        priority, rule = 'Normal', 'N1 No incident conditions'
    return {'priority': priority, 'incident_detected': priority != 'Normal',
            'rule': rule, 'evidence': evidence, 'telemetry': t,
            'timestamp': t['timestamp'], 'scenario': t['scenario']}

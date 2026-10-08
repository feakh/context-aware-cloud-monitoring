"""Synthetic inputs and strict validation; no live cloud collection in this version."""
from datetime import datetime, timezone
import math

SCENARIOS = {
    'normal': ('Normal operation', 30, 45, 50, True, 180, 0),
    'low': ('Isolated CPU increase', 92, 45, 50, True, 180, 0),
    'medium': ('CPU and memory pressure', 92, 91, 50, True, 180, 0),
    'high': ('CPU with slow service and errors', 92, 91, 50, True, 1500, 5),
    'outage': ('Service unavailable', 30, 45, 50, False, 180, 0),
}

def sample(name):
    label, cpu, memory, disk, available, response, errors = SCENARIOS[name]
    return {'timestamp': datetime.now(timezone.utc).isoformat(),
            'scenario': label, 'cpu_percent': cpu, 'memory_percent': memory,
            'disk_percent': disk, 'service_available': available,
            'response_ms': response, 'application_errors': errors}

def validate(data):
    if not isinstance(data, dict):
        raise ValueError('Telemetry must be a JSON object.')
    timestamp = data.get('timestamp')
    if not isinstance(timestamp, str):
        raise ValueError('A timestamp is required.')
    try:
        parsed = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        if parsed.tzinfo is None:
            raise ValueError()
    except ValueError:
        raise ValueError('Timestamp must include a timezone.') from None
    for name in ('cpu_percent', 'memory_percent', 'disk_percent', 'response_ms'):
        value = data.get(name)
        if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
            raise ValueError(f'{name} must be a finite nonnegative number.')
        if name.endswith('_percent') and value > 100:
            raise ValueError(f'{name} cannot exceed 100.')
    if type(data.get('service_available')) is not bool:
        raise ValueError('Service availability must be true or false.')
    if type(data.get('application_errors')) is not int or data['application_errors'] < 0:
        raise ValueError('Application errors must be a nonnegative integer.')
    # Store only the fields needed for this prototype.
    return {name: data[name] for name in ('timestamp', 'cpu_percent', 'memory_percent',
            'disk_percent', 'service_available', 'response_ms', 'application_errors')} | {
            'scenario': str(data.get('scenario', 'Custom synthetic input'))[:100]}

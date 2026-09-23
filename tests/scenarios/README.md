# Controlled Test Scenarios

This directory contains repeatable test scenarios used to evaluate the context-aware cloud infrastructure monitoring prototype.

## Planned Scenario Categories

### Normal Operation

Normal scenarios will generate infrastructure observations that remain within expected operating conditions. These scenarios will be used to evaluate whether the system avoids generating unnecessary incidents.

### Low-Priority Incident

Low-priority scenarios will introduce limited abnormal conditions that satisfy documented Low-priority contextual rules without indicating substantial service degradation.

### Medium-Priority Incident

Medium-priority scenarios will combine multiple abnormal indicators that satisfy documented Medium-priority contextual rules and represent a more significant operational condition.

### High-Priority Incident

High-priority scenarios will combine conditions such as elevated resource utilization, degraded service response, and selected application or system errors to evaluate whether the system correctly identifies and prioritizes more consequential incident conditions.

## Evaluation Measures

Test results will be evaluated using:

- Detection rate
- False-positive rate
- Detection latency
- Priority-classification accuracy

Each scenario will document its expected incident outcome so that the prototype's actual output can be compared with the predefined expected result.

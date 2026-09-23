# Project Scope

## Project Purpose

The project develops a controlled context-aware cloud infrastructure monitoring prototype that evaluates related operational indicators together to detect and prioritize incident conditions for administrator review. The system is intended to support human decision-making rather than replace administrator judgment.

## In Scope

The prototype includes:

- CPU utilization monitoring
- Memory utilization monitoring
- Disk usage monitoring
- Service availability and response-time monitoring
- Selected application and system event monitoring
- Telemetry validation and timestamping
- Contextual rule processing
- Incident detection
- Low, Medium, and High priority classification
- Storage of detected incident information
- Administrator-facing dashboard and reporting
- Controlled normal and incident test scenarios
- Measurement of detection rate, false-positive rate, detection latency, and priority-classification accuracy

## Out of Scope

The prototype does not include:

- Enterprise-scale production deployment
- Autonomous incident remediation
- Production customer data
- Comprehensive multi-cloud support
- Machine-learning model training
- Monitoring of every possible infrastructure metric
- Replacement of administrator judgment

## Project Boundaries

Development and evaluation will occur in a controlled virtualized, containerized, or simulated cloud environment. Synthetic or deliberately generated test information will be used to reduce privacy and security exposure. Contextual rules will remain transparent and reviewable so that incident priorities can be traced to the conditions that produced them.

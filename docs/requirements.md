# System Requirements

## Functional Requirements

**FR-01:** The system shall collect CPU utilization, memory utilization, disk usage, service availability or response time, and selected application/system events from the controlled environment.

**FR-02:** The system shall validate and timestamp collected observations before forwarding them for contextual analysis.

**FR-03:** The system shall evaluate documented combinations of monitored conditions using predefined contextual rules.

**FR-04:** The system shall identify predefined incident conditions when the corresponding contextual rules are satisfied.

**FR-05:** The system shall classify detected incidents into at least three priority levels: Low, Medium, and High.

**FR-06:** Each classified incident shall retain the conditions that contributed to its assigned priority.

**FR-07:** The system shall record an incident timestamp and sufficient contextual information to support subsequent evaluation.

**FR-08:** The dashboard shall allow an authenticated administrator to review detected incidents, assigned priorities, contributing conditions, and timestamps.

**FR-09:** The prototype shall support repeatable normal and predefined incident test scenarios.

**FR-10:** The system shall support administrator decision-making without performing autonomous remediation.

## Non-Functional Requirements

### Performance

The system shall support measurement of detection latency from the occurrence of a predefined incident condition to creation of the corresponding incident record.

### Usability

The dashboard shall present incident priority, timestamp, and contributing conditions together so that an administrator can understand the basis of a classification.

### Reliability

Malformed or unavailable telemetry shall not silently generate a valid incident classification. The prototype will be evaluated using detection rate, false-positive rate, detection latency, and priority-classification accuracy.

### Scalability

Telemetry collection, contextual rule processing, incident detection, priority classification, storage, and presentation shall remain logically separated to support future extension. Enterprise-scale and multi-cloud scalability are outside the scope of the current prototype.

### Security

Administrative access shall require authentication. Access shall follow least-privilege principles, credentials shall remain outside source code, and unnecessary network exposure shall be restricted.

### Privacy

Testing shall use synthetic or deliberately generated information rather than production customer data. Collection and retention shall be limited to information required for incident processing, evaluation, and reporting.

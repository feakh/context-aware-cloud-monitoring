# System Architecture

## Architecture Overview

The context-aware cloud infrastructure monitoring prototype uses a modular pipeline to transform operational telemetry into prioritized incident information for administrator review. The architecture separates data collection, contextual analysis, incident detection, prioritization, storage, and presentation so that individual components can be developed and evaluated independently.

## Architecture Flow

Controlled Cloud-Like Environment
        |
        v
Telemetry Collection and Validation
        |
        v
Contextual Rule Processing
        |
        v
Incident Detection
        |
        v
Priority Classification
        |
        v
Incident Data Store
        |
        v
Dashboard and Reporting
        |
        v
Administrator Review

## Module Responsibilities

### 1. Controlled Cloud-Like Environment

Provides the virtualized, containerized, or simulated infrastructure from which operational observations are generated. The environment supports both normal operating conditions and predefined incident scenarios.

### 2. Telemetry Collection and Validation

Collects selected CPU utilization, memory utilization, disk usage, service availability or response-time information, and selected application/system events. Observations are validated and timestamped before contextual processing.

### 3. Contextual Rule Processing

Evaluates combinations of monitored conditions using predefined and transparent rules. This module allows related indicators to be interpreted together rather than treating every threshold violation as an independent incident.

### 4. Incident Detection

Determines whether the evaluated conditions satisfy a documented incident rule. Detected incidents retain sufficient contextual information to support subsequent evaluation and administrator review.

### 5. Priority Classification

Assigns detected incidents to at least three priority levels: Low, Medium, and High. Classification is based on documented combinations of conditions rather than an opaque machine-learning model.

### 6. Incident Data Store

Stores detected incident records, timestamps, assigned priorities, and contributing conditions required for evaluation and presentation. Collection and retention are limited to information needed by the prototype.

### 7. Dashboard and Reporting

Presents detected incidents, priorities, timestamps, and contributing conditions to an authenticated administrator. The interface supports review and interpretation of incident information.

### 8. Administrator Review

The administrator remains responsible for interpreting incident information and deciding whether operational action is appropriate. The prototype provides decision support and does not perform autonomous remediation.

## Design Principles

The architecture emphasizes modularity, transparency, traceability, security, and human oversight. Separating telemetry collection from contextual interpretation reduces coupling between components and supports controlled testing. Retaining the contributing conditions associated with each incident allows an administrator to understand the basis for a priority classification.

The current prototype is intentionally bounded. Enterprise-scale deployment, comprehensive multi-cloud monitoring, production customer data, autonomous remediation, and machine-learning model training remain outside the project scope.

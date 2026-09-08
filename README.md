# AI Hardware Support Agent

AI Hardware Support Agent is a Python and PowerShell-based system for automated computer hardware diagnostics, configuration monitoring and preventive maintenance.

The project is being developed incrementally, starting with deterministic diagnostics and historical change detection, with the long-term goal of incorporating anomaly detection, monitoring and AI-assisted technical support.

## Project Goals

- Collect hardware information automatically.
- Analyze the current state of the computer.
- Detect hardware configuration changes.
- Detect GPU driver changes.
- Maintain historical diagnostic snapshots.
- Build automated tests.
- Detect anomalies and potential hardware problems.
- Eventually integrate an AI support agent.

## Current Architecture

```text
Windows PC
    |
    v
PowerShell Hardware Collector
    |
    v
hardware_report.json
    |
    v
Python Diagnostic Engine
    |
    v
diagnostics_history.json
    |
    v
Change Detector
    |
    v
Automated Tests

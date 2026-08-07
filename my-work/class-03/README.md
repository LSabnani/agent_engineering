# Class 3 — WidgetWare SDR Context Package

This project implements the Class 3 WidgetWare SDR context package, separating configuration, instructions, context building, and scenario evidence.

## Setup

First, initialize a python virtual environment and install the development dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # macOS/Linux

pip install -e .[dev]
```

## Running Tests

To run the full suite of unit and scenario tests, execute:

```bash
pytest -v
```

## Repository Structure

- `config/`: Contains YAML configuration files (`products.yaml`, `icp.yaml`, `policies.yaml`).
- `docs/`: Centralized business briefs and acceptance criteria.
- `src/widgetware_sdr/`: Contains `instructions.py` (agent persona and guidelines) and `context_builder.py` (deterministic context parser).
- `tests/`: Contains scenario fixtures and unit tests.

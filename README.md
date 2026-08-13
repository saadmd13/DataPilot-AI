# DataPilot AI

**AI-powered autonomous dataset analysis and automation platform**.

DataPilot AI analyzes raw datasets, understands their structure, evaluates data quality, detects ML opportunities, and provides actionable insights and recommendations.

The long-term goal is to build an **autonomous data analyst that can understand and automate dataset preparation.**

---

## Features

* **Dataset Profiling** — Understand rows, columns, data types, statistics, and cardinality.
* **Data Quality Analysis** — Detect missing values, duplicates, constant columns, and other quality issues.
* **Dataset Intelligence** — Generate meaningful dataset-level insights.
* **ML Intelligence** — Detect likely targets, classification/regression problems, and class imbalance.
* **Feature Intelligence** — Analyze feature-target relationships, redundancy, and potential leakage.
* **Recommendations** — Generate prioritized and actionable recommendations.
* **FastAPI API** — Analyze datasets through a REST API.
* **Tested** — 83 automated tests currently passing.

---

## Architecture

```text
Dataset
   ↓
Dataset Profiler
   ↓
Data Quality
   ↓
Dataset Intelligence
   ↓
ML Intelligence
   ↓
Feature Intelligence
   ↓
Quality Score
   ↓
Recommendations
   ↓
Analysis Result
   ↓
FastAPI
```

---

## Tech Stack

**Python · FastAPI · Pydantic · Pandas · NumPy · Pytest**

---

## Getting Started

### 1. Clone

```bash
git clone https://github.com/saadmd13/DataPilot-AI.git
cd DataPilot-AI
```

### 2. Create environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the API

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

## Testing

Run the complete test suite:

```bash
python -m pytest
```

Current status:

```text
83 passed
0 failed
```

---

## Roadmap

* [x] Dataset profiling
* [x] Data quality analysis
* [x] Dataset intelligence
* [x] ML intelligence
* [x] Feature intelligence
* [x] Recommendations
* [x] Unified analysis pipeline
* [x] FastAPI integration
* [ ] Automated data cleaning
* [ ] Automated transformations
* [ ] Feature selection
* [ ] Processed dataset generation
* [ ] AI-powered autonomous workflow
* [ ] Web dashboard

---

## Author

**Saad Mohammed**

GitHub: https://github.com/saadmd13

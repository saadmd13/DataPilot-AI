# DataPilot AI

**AI-powered autonomous dataset analysis and automation platform.**

DataPilot AI analyzes raw datasets, understands their structure, evaluates data quality, detects ML opportunities, generates actionable recommendations, and automatically prepares datasets for further analysis or machine learning.

The long-term goal is to build an **autonomous data analyst that can understand, diagnose, and automate dataset preparation.**

---

## Features

- **Dataset Profiling** — Understand rows, columns, data types, statistics, missing values, and cardinality.
- **Data Quality Analysis** — Detect missing values, duplicates, constant columns, and other quality issues.
- **Dataset Intelligence** — Generate meaningful dataset-level insights.
- **ML Intelligence** — Detect likely targets, classification/regression problems, and class imbalance.
- **Feature Intelligence** — Analyze feature-target relationships and redundant features.
- **Quality Scoring** — Generate an overall dataset quality score.
- **Recommendations** — Generate actionable recommendations based on dataset conditions.
- **Automated Data Preparation** — Plan and execute safe dataset transformations.
- **Transformation Planning** — Automatically determine appropriate transformations for detected issues.
- **Transformation Execution** — Apply planned transformations without modifying the original dataset.
- **Processed Dataset Generation** — Save prepared datasets for further analysis or machine learning.
- **Processed Dataset Download** — Retrieve generated datasets through the API.
- **FastAPI Backend** — Analyze datasets through a REST API.
- **Streamlit Dashboard** — Interactive interface for uploading and exploring datasets.
- **Automated Testing** — 100+ tests covering the core backend and analysis pipeline.

---

## Architecture

```text
Dataset Upload
      ↓
Dataset Profiler
      ↓
Data Quality Analysis
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
Transformation Planner
      ↓
Transformation Executor
      ↓
Processed Dataset
      ↓
FastAPI / Streamlit
````

---

## Tech Stack

**Python · FastAPI · Streamlit · Pydantic · Pandas · NumPy · Scikit-learn · Pytest**

---

## Project Structure

```text
DataPilot-AI/
│
├── app/
│   ├── api/
│   ├── models/
│   ├── services/
│   ├── tools/
│   └── utils/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── frontend/
│   └── streamlit_app.py
│
├── tests/
│
├── reports/
├── visualizations/
│
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## Getting Started

### 1. Clone

```bash
git clone https://github.com/saadmd13/DataPilot-AI.git
cd DataPilot-AI
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

Windows:

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Backend

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Run the Dashboard

In a separate terminal:

```bash
streamlit run frontend/streamlit_app.py
```

The dashboard allows datasets to be uploaded and analyzed through the DataPilot backend.

Supported dataset formats include:

```text
CSV
XLSX
XLS
JSON
```

---

## Testing

Run the complete test suite:

```bash
python -m pytest
```

Current project status:

```text
100+ tests
0 failed
```

The test suite covers areas including:

* Dataset profiling
* Data quality analysis
* Dataset intelligence
* ML intelligence
* Feature intelligence
* Analysis pipeline
* Data preparation
* Transformation planning
* Transformation execution
* Processed dataset generation
* API endpoints
* Dataset downloads
* Validation and configuration

---

## Example Workflow

A dataset can move through the following workflow automatically:

```text
Raw Dataset
    ↓
Profile Dataset
    ↓
Detect Quality Issues
    ↓
Generate Intelligence
    ↓
Detect ML Opportunities
    ↓
Analyze Features
    ↓
Calculate Quality Score
    ↓
Generate Recommendations
    ↓
Plan Transformations
    ↓
Execute Transformations
    ↓
Generate Processed Dataset
```

For example, DataPilot can detect:

```text
Missing values
Duplicates
Constant columns
Identifier columns
Target columns
Class imbalance
Feature relationships
Redundant features
```

and generate transformations such as:

```text
Median imputation
Mode imputation
Duplicate removal
Constant column removal
Identifier exclusion
```

The original DataFrame is preserved while the prepared dataset is generated separately.

---

## Roadmap

* [x] Dataset profiling
* [x] Data quality analysis
* [x] Dataset intelligence
* [x] ML intelligence
* [x] Feature intelligence
* [x] Quality scoring
* [x] Recommendations
* [x] Unified analysis pipeline
* [x] FastAPI integration
* [x] Automated data preparation
* [x] Transformation planning
* [x] Transformation execution
* [x] Processed dataset generation
* [x] Processed dataset download
* [x] Streamlit dashboard
* [ ] Advanced feature selection
* [ ] ML readiness scoring
* [ ] Advanced statistical intelligence
* [ ] Data leakage detection improvements
* [ ] Advanced preprocessing strategies
* [ ] AI-powered autonomous workflow

---

## Current Status

DataPilot AI is actively under development.

The core backend has evolved from a dataset profiling system into a broader **dataset intelligence and automated preparation pipeline** capable of analyzing datasets, generating insights and recommendations, executing safe transformations, and producing processed datasets.

The next stage is expanding the intelligence layer and moving toward a more autonomous data analysis workflow.

---

## Author

**Saad Mohammed**

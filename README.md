DataPilot AI

«AI-powered autonomous dataset analysis and automation platform»

DataPilot AI is an intelligent data-analysis platform designed to automatically understand datasets, evaluate data quality, detect machine-learning opportunities, identify important feature relationships, generate actionable recommendations, and expose the entire analysis pipeline through an API.

The goal is to move beyond traditional data profiling and build an autonomous system that can understand a dataset and eventually automate the data-preparation workflow.

---

🚀 Current Capabilities

DataPilot AI currently provides:

- Dataset profiling
- Column-level semantic intelligence
- Missing-value analysis
- Duplicate detection
- Constant-column detection
- Identifier detection
- Value-pattern detection
- Dataset-level intelligence
- Data-quality scoring
- Automated data-quality grading
- Risk-level assessment
- Automated recommendations
- Machine-learning problem detection
- Target-column detection
- Classification analysis
- Regression analysis
- Class-imbalance detection
- Feature-target relationship analysis
- Feature redundancy detection
- Potential data-leakage detection
- Unified dataset analysis pipeline
- FastAPI REST API
- Automated test coverage

---

🧠 Architecture

                         DATASET
                            │
                            ▼
                     ┌─────────────┐
                     │ File Loader │
                     └──────┬──────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │ Dataset Profiler │
                  └────────┬─────────┘
                           │
             ┌─────────────┼──────────────┐
             ▼             ▼              ▼
      Data Quality    Column          Dataset
       Analyzer     Intelligence    Intelligence
             │             │              │
             └─────────────┼──────────────┘
                           │
                           ▼
                  ┌────────────────┐
                  │ Quality Scorer │
                  └───────┬────────┘
                          │
                          ▼
                  ┌────────────────┐
                  │ ML Intelligence│
                  └───────┬────────┘
                          │
                    Target Detection
                          │
                          ▼
                ┌────────────────────┐
                │Feature Intelligence│
                └─────────┬──────────┘
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
        Target         Feature      Potential
     Relationships    Redundancy     Leakage
             │            │            │
             └────────────┼────────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Recommendations │
                 └────────┬────────┘
                          │
                          ▼
                 ┌────────────────┐
                 │ AnalysisResult │
                 └────────┬───────┘
                          │
                          ▼
                    FastAPI API

---

🔍 Dataset Profiling

The dataset profiler automatically generates a structured profile containing:

Dataset-level information

- Filename
- Row count
- Column count
- Memory usage
- Duplicate rows
- Missing values
- Dataset composition

Column-level information

- Pandas data type
- Semantic type
- Missing count
- Missing percentage
- Unique count
- Unique percentage
- Cardinality ratio
- Identifier status
- Identifier confidence
- Datetime parsing success
- Value patterns
- Pattern confidence
- Pattern match percentage
- Pattern examples

Numeric statistics

- Minimum
- Maximum
- Mean
- Median
- Standard deviation

Categorical statistics

- Top values
- Value frequencies

Text statistics

- Minimum length
- Maximum length
- Average length

---

🧹 Data Quality Analysis

DataPilot evaluates the structural quality of a dataset.

Current checks include:

- Missing cells
- Missing percentage
- Duplicate rows
- Duplicate percentage
- Constant columns
- Column-level uniqueness
- Column-level missing values

Example:

Quality Score: 93.62/100
Grade: A
Risk Level: low

The quality system also produces:

- Completeness score
- Uniqueness score
- Consistency score
- Validity score
- Overall score
- Grade
- Risk level
- Issue counts
- Strengths
- Weaknesses

---

🧬 Column Intelligence

DataPilot analyzes individual columns and generates contextual insights.

Examples include:

Identifier detection

customer_id appears to be an identifier column.

Missing values

age contains 60.00% missing values.

Constant columns

country contains only one unique value.

High cardinality

email has a cardinality ratio of 1.00.

Value patterns

email appears to contain email values.

Identifier detection intentionally does not treat every 100%-unique column as an identifier.

For example, a scientific measurement can have 100% unique values without being an ID.

---

🔎 Value Pattern Detection

The pattern detection engine identifies structured values inside columns.

The engine can detect patterns such as:

- Email
- Phone
- UUID
- URL
- Date-like values
- Other configured structured formats

Pattern detection returns:

pattern
confidence
matched_count
total_count
match_percentage
examples

A pattern must meet the configured confidence threshold before being treated as a dominant column pattern.

---

💡 Dataset Intelligence

Dataset Intelligence provides higher-level observations about the entire dataset.

Examples:

Potential identifier columns: customer_id

The dataset contains 100 rows and 6 columns:
2 numeric, 1 categorical, 1 text, 1 datetime, and 1 boolean.

It can also identify:

- Empty datasets
- Missing-value problems
- Duplicate rows
- Constant columns
- Identifier columns
- Detected value patterns
- Dataset composition

---

🤖 ML Intelligence

DataPilot now includes a dedicated machine-learning intelligence layer.

The ML engine analyzes datasets and attempts to determine:

Target column

It identifies likely target variables based on dataset structure and known target naming patterns.

Example:

target_class

Problem type

DataPilot can identify:

binary_classification
multiclass_classification
regression

Class imbalance

For classification datasets, the engine analyzes target distribution.

Example:

Class 0: 90.80%
Class 1: 9.20%

Imbalance ratio: approximately 9.87:1

This can generate a high-severity ML insight when imbalance is significant.

---

📊 Feature Intelligence

Feature Intelligence builds on ML Intelligence.

Once a target column has been identified, DataPilot analyzes relationships between features and the target.

Current capabilities include:

Feature-target correlation

Example:

Feature 'Excess kurtosis of the integrated profile'
has a strong positive relationship with target 'target_class'
(correlation=0.792).

Relationship strength

Correlations are classified as:

Minimal
Weak
Moderate
Strong

Direction

Relationships are identified as:

Positive
Negative

Feature redundancy

DataPilot detects highly correlated feature pairs.

Example:

Excess kurtosis of the integrated profile
↔
Skewness of the integrated profile

Correlation: 0.945

Potential data leakage

Features with extremely strong target relationships can be flagged for investigation.

---

🧪 Real Dataset Validation

The Feature Intelligence engine has been tested against the Pulsar dataset.

Example findings included:

Mean of the integrated profile
Correlation: -0.676
Relationship: moderate negative

Excess kurtosis of the integrated profile
Correlation: +0.792
Relationship: strong positive

Skewness of the integrated profile
Correlation: +0.707
Relationship: strong positive

The engine also detected highly correlated feature pairs:

Integrated-profile kurtosis ↔ integrated-profile skewness
Correlation: 0.945

DM-SNR kurtosis ↔ DM-SNR skewness
Correlation: 0.924

This demonstrates that DataPilot's intelligence layer is being validated against real-world datasets rather than only synthetic unit-test data.

---

🧠 Recommendations Engine

DataPilot converts analysis results into actionable recommendations.

Example:

[CRITICAL] Handle missing values in 'age'

Type:
missing_values

Action:
Consider median imputation for missing numeric values.

Confidence:
0.95

Another example:

[LOW] Treat 'customer_id' as an identifier

Action:
Use this column as a record identifier rather than as a
predictive feature unless there is a specific reason to use it.

Recommendations contain:

- Recommendation type
- Priority
- Column name
- Title
- Description
- Recommended action
- Confidence

---

🔗 Unified Analysis Pipeline

The central "DataPilotAnalyzer" combines the individual intelligence engines.

The pipeline performs:

1. Dataset profiling
2. Data quality analysis
3. Dataset intelligence
4. ML intelligence
5. Target detection
6. Feature intelligence
7. Quality scoring
8. Recommendation generation
9. Unified result construction

The final result is represented by "AnalysisResult".

Conceptually:

{
  "filename": "dataset.csv",
  "profile": {},
  "quality_report": {},
  "quality_score": {},
  "insights": [],
  "ml_insights": [],
  "feature_insights": [],
  "recommendations": []
}

---

🌐 FastAPI

DataPilot exposes its analysis functionality through FastAPI.

Base endpoints

GET /
GET /health
POST /dataset/upload

Analysis endpoint

POST /api/v1/analyze

The analysis endpoint accepts a dataset upload and runs the complete DataPilot pipeline.

The response uses the "AnalysisResult" model.

---

📁 Project Structure

DataPilot-AI/
│
├── app/
│   ├── api/
│   │   └── analysis.py
│   │
│   ├── models/
│   │   ├── analysis_result.py
│   │   ├── column_insight.py
│   │   ├── data_quality.py
│   │   ├── dataset_insight.py
│   │   ├── dataset_profile.py
│   │   ├── feature_insight.py
│   │   ├── ml_insight.py
│   │   ├── quality_score.py
│   │   ├── recommendation.py
│   │   └── value_pattern.py
│   │
│   ├── services/
│   │   ├── analysis_pipeline.py
│   │   ├── column_intelligence.py
│   │   ├── data_quality_analyzer.py
│   │   ├── dataset_intelligence.py
│   │   ├── dataset_profiler.py
│   │   ├── feature_intelligence.py
│   │   ├── ml_intelligence.py
│   │   ├── pattern_detector.py
│   │   ├── quality_score_engine.py
│   │   └── recommendation_engine.py
│   │
│   ├── tools/
│   │   └── file_loader.py
│   │
│   ├── utils/
│   │   ├── file_utils.py
│   │   └── logger.py
│   │
│   ├── config.py
│   └── main.py
│
├── tests/
│   ├── test_analysis_pipeline.py
│   ├── test_api.py
│   ├── test_column_intelligence.py
│   ├── test_config.py
│   ├── test_data_quality.py
│   ├── test_dataset_intelligence.py
│   ├── test_dataset_profiler.py
│   ├── test_feature_intelligence.py
│   ├── test_file_loader.py
│   ├── test_file_utils.py
│   ├── test_ml_intelligence.py
│   ├── test_pattern_detector.py
│   ├── test_quality_score_engine.py
│   ├── test_recommendation_engine.py
│   └── test_validators.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── outputs/
│
├── reports/
├── visualizations/
│
├── pytest.ini
├── requirements.txt
└── README.md

---

🛠️ Technology Stack

Backend

- Python 3.12
- FastAPI
- Pydantic
- Pydantic Settings

Data Processing

- pandas
- NumPy

Testing

- pytest
- pytest-anyio

Development

- Git
- GitHub
- Uvicorn

---

⚙️ Installation

Clone the repository:

git clone https://github.com/saadmd13/DataPilot-AI.git
cd DataPilot-AI

Create a virtual environment:

python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

---

▶️ Running DataPilot AI

Start the FastAPI development server:

uvicorn app.main:app --reload

Open the API documentation:

http://127.0.0.1:8000/docs

The Swagger interface can be used to upload datasets and test:

POST /api/v1/analyze

---

🧪 Running Tests

Run the complete test suite:

python -m pytest

Current project status:

83 tests passed
1 warning
0 failures

Run a specific test module:

python -m pytest tests/test_feature_intelligence.py

Run ML intelligence tests:

python -m pytest tests/test_ml_intelligence.py

Run the pipeline tests:

python -m pytest tests/test_analysis_pipeline.py

---

📈 Current Development Status

Phase 1 — Foundation

- [x] Project structure
- [x] Configuration
- [x] Logging
- [x] File utilities
- [x] Dataset loading
- [x] Upload API

Phase 2 — Dataset Understanding

- [x] Dataset profiling
- [x] Column profiling
- [x] Semantic type detection
- [x] Datetime detection
- [x] Identifier detection
- [x] Value-pattern detection
- [x] Data-quality analysis

Phase 3 — Intelligence

- [x] Dataset intelligence
- [x] Column intelligence
- [x] Quality scoring
- [x] Risk assessment
- [x] Recommendation engine

Phase 4 — Machine Learning Intelligence

- [x] Target detection
- [x] Classification detection
- [x] Regression detection
- [x] Class imbalance detection
- [x] ML insight model

Phase 5 — Feature Intelligence

- [x] Feature-target relationships
- [x] Correlation analysis
- [x] Relationship-strength classification
- [x] Feature redundancy detection
- [x] Potential leakage detection
- [x] Feature insight model
- [x] Pipeline integration

Phase 6 — Dataset Automation

- [ ] Automated missing-value treatment
- [ ] Automated duplicate handling
- [ ] Categorical encoding
- [ ] Numerical transformations
- [ ] Outlier detection and treatment
- [ ] Feature selection
- [ ] Automated preprocessing pipeline
- [ ] Processed dataset generation
- [ ] Transformation report

Phase 7 — AI Agent Layer

- [ ] Autonomous analysis planning
- [ ] Natural-language dataset explanations
- [ ] AI-assisted transformation decisions
- [ ] Automated workflow execution
- [ ] Human approval checkpoints
- [ ] End-to-end dataset automation

Phase 8 — Production Platform

- [ ] Modern web dashboard
- [ ] Dataset history
- [ ] Analysis persistence
- [ ] Visualization engine
- [ ] Report generation
- [ ] User authentication
- [ ] Background processing
- [ ] Production deployment

---

🎯 Vision

DataPilot AI is being developed toward an autonomous data analyst/data-preparation agent.

Instead of requiring a user to manually:

Upload dataset
      ↓
Inspect columns
      ↓
Find missing values
      ↓
Check duplicates
      ↓
Understand data types
      ↓
Find target
      ↓
Analyze ML suitability
      ↓
Analyze features
      ↓
Decide transformations
      ↓
Clean dataset
      ↓
Build preprocessing pipeline

DataPilot aims to automate this workflow:

                 ┌──────────────────┐
                 │   Upload Dataset │
                 └────────┬─────────┘
                          ↓
                 ┌──────────────────┐
                 │ Understand Data  │
                 └────────┬─────────┘
                          ↓
                 ┌──────────────────┐
                 │ Detect Problems  │
                 └────────┬─────────┘
                          ↓
                 ┌──────────────────┐
                 │ Explain Findings │
                 └────────┬─────────┘
                          ↓
                 ┌──────────────────┐
                 │ Recommend Actions│
                 └────────┬─────────┘
                          ↓
                 ┌──────────────────┐
                 │ Automate Changes │
                 └────────┬─────────┘
                          ↓
                 ┌──────────────────┐
                 │ Processed Dataset│
                 └──────────────────┘

The long-term objective is to make DataPilot capable of taking a raw dataset and autonomously determining what it contains, what is wrong with it, what should be done, why those actions are appropriate, and how to produce a machine-learning-ready dataset.

---

👨‍💻 Author

Saad Mohammed

GitHub: "@saadmd13" (https://github.com/saadmd13)

---

📄 License

License information will be added as the project approaches its first public release.

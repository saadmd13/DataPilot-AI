from __future__ import annotations

import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000"
REQUEST_TIMEOUT = 120


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="DataPilot AI",
    page_icon="D",
    layout="wide",
)


# ============================================================
# GLOBAL CSS
# ============================================================

st.html(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {
        background: #ffffff;
        color: #111111;
    }

    .block-container {
        max-width: 1380px;
        padding-top: 2rem;
        padding-bottom: 5rem;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* Streamlit default text */
    .stApp,
    .stApp p,
    .stApp label,
    .stApp span,
    .stApp div {
        color: #111111;
    }

    /* ========================================================
       HERO
       ======================================================== */

    .dp-hero {
        position: relative;
        overflow: hidden;

        padding: 44px 48px;

        margin-bottom: 32px;

        border-radius: 22px;

        border: 1px solid #e5e7eb;

        background: #ffffff;

        box-shadow:
            0 8px 30px rgba(0, 0, 0, 0.06);
    }

    .dp-hero::after {
        content: "";

        position: absolute;

        width: 300px;
        height: 300px;

        right: -120px;
        top: -160px;

        border-radius: 50%;

        background: #f3f4f6;
    }

    .dp-brand {
        position: relative;
        z-index: 2;

        font-size: 3rem;
        font-weight: 800;

        letter-spacing: -0.045em;

        color: #000000 !important;
    }

    .dp-brand span {
        color: #000000 !important;
    }

    .dp-description {
        position: relative;
        z-index: 2;

        max-width: 720px;

        margin-top: 12px;

        color: #555555 !important;

        font-size: 1rem;

        line-height: 1.7;
    }

    .dp-pills {
        position: relative;
        z-index: 2;

        display: flex;

        flex-wrap: wrap;

        gap: 9px;

        margin-top: 25px;
    }

    .dp-pill {
        padding: 7px 12px;

        border-radius: 999px;

        background: #f5f5f5;

        border: 1px solid #e5e5e5;

        color: #222222 !important;

        font-size: 0.75rem;

        font-weight: 600;
    }

    .dp-pill.online {
        background: #f3f4f3;

        border-color: #d6d6d6;

        color: #111111 !important;
    }


    /* ========================================================
       SECTION
       ======================================================== */

    .dp-section {
        margin-top: 38px;
        margin-bottom: 18px;
    }

    .dp-section-title {
        color: #000000 !important;

        font-size: 1.45rem;

        font-weight: 750;

        letter-spacing: -0.02em;
    }

    .dp-section-subtitle {
        margin-top: 4px;

        color: #666666 !important;

        font-size: 0.82rem;
    }


    /* ========================================================
       METRICS
       ======================================================== */

    .dp-grid {
        display: grid;

        grid-template-columns:
            repeat(4, minmax(0, 1fr));

        gap: 15px;
    }

    .dp-card {
        min-height: 135px;

        padding: 22px;

        border-radius: 16px;

        border: 1px solid #e5e7eb;

        background: #ffffff;

        box-shadow:
            0 4px 16px rgba(0, 0, 0, 0.04);
    }

    .dp-label {
        color: #666666 !important;

        font-size: 0.72rem;

        text-transform: uppercase;

        letter-spacing: 0.08em;

        font-weight: 650;
    }

    .dp-value {
        margin-top: 12px;

        color: #000000 !important;

        font-size: 2rem;

        font-weight: 750;

        letter-spacing: -0.03em;
    }

    .dp-small {
        margin-top: 5px;

        color: #777777 !important;

        font-size: 0.75rem;
    }


    /* ========================================================
       INSIGHT
       ======================================================== */

    .dp-insight {
        padding: 18px 20px;

        margin-bottom: 10px;

        border-radius: 14px;

        background: #ffffff;

        border: 1px solid #e5e7eb;

        box-shadow:
            0 3px 12px rgba(0, 0, 0, 0.03);
    }

    .dp-insight-top {
        display: flex;

        align-items: center;

        gap: 9px;

        margin-bottom: 9px;
    }

    .dp-badge {
        padding: 4px 8px;

        border-radius: 999px;

        font-size: 0.65rem;

        font-weight: 700;

        text-transform: uppercase;
    }

    .dp-info {
        background: #f1f1f1;

        color: #111111 !important;
    }

    .dp-warning {
        background: #eeeeee;

        color: #111111 !important;
    }

    .dp-critical {
        background: #e7e7e7;

        color: #000000 !important;
    }

    .dp-insight-type {
        color: #111111 !important;

        font-size: 0.82rem;

        font-weight: 700;
    }

    .dp-insight-column {
        color: #777777 !important;

        font-size: 0.75rem;
    }

    .dp-insight-message {
        color: #333333 !important;

        font-size: 0.86rem;

        line-height: 1.6;
    }


    /* ========================================================
       PREPARATION
       ======================================================== */

    .dp-prep {
        padding: 25px;

        border-radius: 18px;

        background: #fafafa;

        border: 1px solid #e5e7eb;
    }

    .dp-transform {
        padding: 10px 0;

        border-bottom:
            1px solid #e5e7eb;

        color: #333333 !important;

        font-size: 0.83rem;
    }

    .dp-success {
        margin-top: 18px;

        padding: 13px 15px;

        border-radius: 10px;

        background: #f3f3f3;

        color: #111111 !important;

        font-size: 0.82rem;

        font-weight: 650;
    }


    /* ========================================================
       PROCESSED DATASET
       ======================================================== */

    .dp-file {
        padding: 25px;

        border-radius: 18px;

        background: #fafafa;

        border: 1px solid #e5e7eb;
    }

    .dp-file-label {
        color: #666666 !important;

        font-size: 0.7rem;

        text-transform: uppercase;

        letter-spacing: 0.08em;
    }

    .dp-file-name {
        display: inline-block;

        margin-top: 8px;

        padding: 7px 10px;

        border-radius: 8px;

        background: #f1f1f1;

        color: #111111 !important;

        font-family: monospace;

        font-size: 0.8rem;
    }


    /* ========================================================
       STREAMLIT WIDGETS
       ======================================================== */

    /* Buttons */

    .stButton > button {
        background: #000000 !important;

        color: #ffffff !important;

        border: 1px solid #000000 !important;

        border-radius: 10px;

        font-weight: 650;
    }

    .stButton > button:hover {
        background: #222222 !important;

        color: #ffffff !important;

        border-color: #222222 !important;
    }

    .stButton > button p {
        color: #ffffff !important;
    }


    /* Download button */

    .stDownloadButton > button {
        background: #000000 !important;

        color: #ffffff !important;

        border: 1px solid #000000 !important;

        border-radius: 10px;

        font-weight: 650;
    }

    .stDownloadButton > button p {
        color: #ffffff !important;
    }


    /* File uploader */

    [data-testid="stFileUploader"] {
        background: #ffffff;
        border-radius: 14px;
    }

    [data-testid="stFileUploaderDropzone"] {
        background: #fafafa !important;

        border: 1px dashed #cfcfcf !important;

        border-radius: 14px !important;
    }

    [data-testid="stFileUploaderDropzone"] * {
        color: #222222 !important;
    }


    /* Dataframe */

    [data-testid="stDataFrame"] {
        border: 1px solid #e5e7eb;
        border-radius: 12px;
    }


    /* Expanders */

    [data-testid="stExpander"] {
        background: #ffffff;

        border: 1px solid #e5e7eb;

        border-radius: 12px;
    }

    [data-testid="stExpander"] summary {
        color: #111111 !important;
    }


    /* Metrics */

    [data-testid="stMetric"] {
        background: #ffffff;

        border: 1px solid #e5e7eb;

        border-radius: 14px;

        padding: 15px;
    }

    [data-testid="stMetricLabel"] {
        color: #666666 !important;
    }

    [data-testid="stMetricValue"] {
        color: #000000 !important;
    }


    /* Alerts */

    [data-testid="stAlert"] {
        color: #111111 !important;
    }

    [data-testid="stAlert"] p {
        color: #111111 !important;
    }


    /* ========================================================
       RESPONSIVE
       ======================================================== */

    @media (max-width: 900px) {

        .dp-grid {
            grid-template-columns:
                repeat(2, minmax(0, 1fr));
        }

        .dp-brand {
            font-size: 2.3rem;
        }

        .dp-hero {
            padding: 32px;
        }

    }

    </style>
    """
)


# ============================================================
# HELPERS
# ============================================================

def format_number(value):
    if value is None:
        return "—"

    try:
        return f"{int(value):,}"
    except (TypeError, ValueError):
        return str(value)


def format_percentage(value):
    if value is None:
        return "—"

    try:
        return f"{float(value):.2f}%"
    except (TypeError, ValueError):
        return str(value)


def get_error(response):
    try:
        data = response.json()

        if isinstance(data, dict):
            return data.get(
                "detail",
                "Request failed.",
            )

    except ValueError:
        pass

    return response.text or "Request failed."


def render_section(title, subtitle):
    st.html(
        f"""
        <div class="dp-section">

            <div class="dp-section-title">
                {title}
            </div>

            <div class="dp-section-subtitle">
                {subtitle}
            </div>

        </div>
        """
    )


def render_metric(label, value, subtitle):
    st.html(
        f"""
        <div class="dp-card">

            <div class="dp-label">
                {label}
            </div>

            <div class="dp-value">
                {value}
            </div>

            <div class="dp-small">
                {subtitle}
            </div>

        </div>
        """
    )


def render_insight(insight):

    severity = str(
        insight.get(
            "severity",
            "info",
        )
    ).lower()

    if severity not in {
        "info",
        "warning",
        "critical",
    }:
        severity = "info"

    insight_type = insight.get(
        "insight_type",
        "insight",
    )

    column = (
        insight.get("column_name")
        or insight.get("feature_name")
        or insight.get("target_column")
        or ""
    )

    message = insight.get(
        "message",
        "",
    )

    confidence = insight.get(
        "confidence"
    )

    confidence_html = ""

    if confidence is not None:

        try:

            confidence_html = (
                f"""
                <div style="
                    margin-top:8px;
                    color:#777777;
                    font-size:0.72rem;
                ">
                    Confidence:
                    {float(confidence) * 100:.0f}%
                </div>
                """
            )

        except (
            TypeError,
            ValueError,
        ):
            pass

    st.html(
        f"""
        <div class="dp-insight">

            <div class="dp-insight-top">

                <span class="
                    dp-badge
                    dp-{severity}
                ">
                    {severity}
                </span>

                <span class="dp-insight-type">
                    {insight_type}
                </span>

                <span class="dp-insight-column">
                    {column}
                </span>

            </div>

            <div class="dp-insight-message">
                {message}
            </div>

            {confidence_html}

        </div>
        """
    )


# ============================================================
# HERO
# ============================================================

st.html(
    """
    <div class="dp-hero">

        <div class="dp-brand">
            Data<span>Pilot</span> AI
        </div>

        <div class="dp-description">
            Turn raw datasets into structured intelligence,
            actionable recommendations, and production-ready
            processed data.
        </div>

        <div class="dp-pills">

            <span class="dp-pill online">
                Analysis Engine Online
            </span>

            <span class="dp-pill">
                Automated Profiling
            </span>

            <span class="dp-pill">
                ML Intelligence
            </span>

            <span class="dp-pill">
                Feature Intelligence
            </span>

            <span class="dp-pill">
                Data Preparation
            </span>

        </div>

    </div>
    """
)


# ============================================================
# BACKEND STATUS
# ============================================================

backend_online = False

try:

    health = requests.get(
        f"{API_URL}/health",
        timeout=5,
    )

    backend_online = (
        health.status_code == 200
    )

except requests.RequestException:

    backend_online = False


if backend_online:

    st.success(
        "DataPilot backend connected."
    )

else:

    st.error(
        "Backend is offline. Run: "
        "`uvicorn app.main:app --reload`"
    )


# ============================================================
# UPLOAD
# ============================================================

render_section(
    "Analyze a dataset",
    "Upload a dataset and let DataPilot handle the analysis.",
)


uploaded_file = st.file_uploader(
    "Upload dataset",
    type=[
        "csv",
        "xlsx",
        "xls",
        "json",
    ],
)


if uploaded_file:

    col1, col2 = st.columns(
        [4, 1]
    )

    with col1:

        st.write(
            f"Selected: **{uploaded_file.name}**"
        )

    with col2:

        st.write(
            f"{uploaded_file.size:,} bytes"
        )

    if st.button(
        "Run DataPilot Analysis",
        type="primary",
        use_container_width=True,
        disabled=not backend_online,
    ):

        with st.spinner(
            "DataPilot is analyzing your dataset..."
        ):

            try:

                response = requests.post(
                    f"{API_URL}/api/v1/analyze",
                    files={
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            uploaded_file.type
                            or "application/octet-stream",
                        )
                    },
                    timeout=REQUEST_TIMEOUT,
                )

                if response.status_code != 200:

                    st.error(
                        get_error(response)
                    )

                else:

                    st.session_state[
                        "analysis_result"
                    ] = response.json()

                    st.success(
                        "Analysis completed successfully."
                    )

            except requests.RequestException as exc:

                st.error(
                    f"Could not connect to DataPilot: {exc}"
                )


# ============================================================
# RESULT
# ============================================================

result = st.session_state.get(
    "analysis_result"
)


if result is None:

    st.html(
        """
        <div style="
            margin-top:45px;
            padding:45px;
            text-align:center;
            border-radius:20px;
            background:#ffffff;
            border:1px solid #e5e7eb;
            box-shadow:0 4px 20px rgba(0,0,0,0.04);
        ">

            <div style="
                color:#000000;
                font-size:1.1rem;
                font-weight:700;
            ">
                Analysis workspace ready
            </div>

            <div style="
                margin-top:8px;
                color:#666666;
                font-size:0.84rem;
            ">
                Upload a dataset above to begin.
            </div>

        </div>
        """
    )

    st.stop()


# ============================================================
# DATA
# ============================================================

profile = result.get(
    "profile",
    {},
)

quality = result.get(
    "quality_report",
    {},
)

score = result.get(
    "quality_score",
    {},
)

ml_insights = result.get(
    "ml_insights",
    [],
)

feature_insights = result.get(
    "feature_insights",
    [],
)

dataset_insights = result.get(
    "insights",
    [],
)

recommendations = result.get(
    "recommendations",
    [],
)

preparation = result.get(
    "preparation"
)

processed = result.get(
    "processed_dataset"
)


# ============================================================
# OVERVIEW
# ============================================================

render_section(
    "Dataset Overview",
    "A quick snapshot of the dataset DataPilot analyzed.",
)


rows = profile.get(
    "row_count",
    0,
)

columns = profile.get(
    "column_count",
    0,
)

missing = profile.get(
    "missing_percentage",
    quality.get(
        "missing_percentage",
        0,
    ),
)

quality_score = score.get(
    "overall_score",
    0,
)


m1, m2, m3, m4 = st.columns(4)

with m1:
    render_metric(
        "Rows",
        format_number(rows),
        "Records analyzed",
    )

with m2:
    render_metric(
        "Columns",
        format_number(columns),
        "Features detected",
    )

with m3:
    render_metric(
        "Quality Score",
        f"{float(quality_score):.1f}",
        "Overall dataset health",
    )

with m4:
    render_metric(
        "Missing Data",
        format_percentage(missing),
        "Across all cells",
    )


# ============================================================
# COLUMN TABLE
# ============================================================

render_section(
    "Column Intelligence",
    "Types, completeness and uniqueness across your dataset.",
)


column_rows = []

for column in profile.get(
    "columns",
    [],
):

    column_rows.append(
        {
            "Column": column.get(
                "name",
                "—",
            ),
            "Type": column.get(
                "semantic_type",
                "—",
            ),
            "Missing": format_number(
                column.get(
                    "missing_count",
                    0,
                )
            ),
            "Missing %": format_percentage(
                column.get(
                    "missing_percentage",
                    0,
                )
            ),
            "Unique": format_number(
                column.get(
                    "unique_count",
                    0,
                )
            ),
        }
    )


if column_rows:

    st.dataframe(
        column_rows,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# QUALITY
# ============================================================

render_section(
    "Data Quality",
    "Structural checks performed by the DataPilot quality engine.",
)


q1, q2, q3 = st.columns(3)

with q1:

    st.metric(
        "Missing Cells",
        format_number(
            quality.get(
                "missing_cells",
                0,
            )
        ),
    )

with q2:

    st.metric(
        "Duplicate Rows",
        format_number(
            quality.get(
                "duplicate_rows",
                0,
            )
        ),
    )

with q3:

    st.metric(
        "Constant Columns",
        format_number(
            len(
                quality.get(
                    "constant_columns",
                    [],
                )
            )
        ),
    )


# ============================================================
# ML INTELLIGENCE
# ============================================================

render_section(
    "ML Intelligence",
    "Automatically detected machine-learning signals.",
)


if ml_insights:

    for insight in ml_insights:

        render_insight(
            insight
        )

else:

    st.info(
        "No ML insights detected."
    )


# ============================================================
# FEATURE INTELLIGENCE
# ============================================================

render_section(
    "Feature Intelligence",
    "Relationships and potential feature-level issues.",
)


if feature_insights:

    for insight in feature_insights:

        render_insight(
            insight
        )

else:

    st.info(
        "No feature insights detected."
    )


# ============================================================
# DATASET INTELLIGENCE
# ============================================================

if dataset_insights:

    render_section(
        "Dataset Intelligence",
        "Structural observations about the dataset.",
    )

    for insight in dataset_insights:

        render_insight(
            insight
        )


# ============================================================
# RECOMMENDATIONS
# ============================================================

render_section(
    "Recommendations",
    "Actions suggested by DataPilot based on the analysis.",
)


if recommendations:

    for index, recommendation in enumerate(
        recommendations,
        start=1,
    ):

        title = recommendation.get(
            "title",
            recommendation.get(
                "recommendation",
                f"Recommendation {index}",
            ),
        )

        message = recommendation.get(
            "message",
            recommendation.get(
                "description",
                "",
            ),
        )

        with st.expander(
            f"{index}. {title}"
        ):

            st.write(
                message
            )

else:

    st.info(
        "No recommendations generated."
    )


# ============================================================
# PREPARATION
# ============================================================

if preparation:

    render_section(
        "Automated Data Preparation",
        "Safe transformations applied automatically.",
    )

    prep_rows = preparation.get(
        "original_row_count",
        0,
    )

    final_rows = preparation.get(
        "final_row_count",
        0,
    )

    prep_columns = preparation.get(
        "original_column_count",
        0,
    )

    final_columns = preparation.get(
        "final_column_count",
        0,
    )

    transformations = preparation.get(
        "transformations",
        [],
    )

    p1, p2, p3 = st.columns(3)

    with p1:

        st.metric(
            "Rows",
            f"{format_number(prep_rows)} → "
            f"{format_number(final_rows)}",
        )

    with p2:

        st.metric(
            "Columns",
            f"{format_number(prep_columns)} → "
            f"{format_number(final_columns)}",
        )

    with p3:

        st.metric(
            "Transformations",
            format_number(
                preparation.get(
                    "transformations_applied",
                    len(transformations),
                )
            ),
        )

    st.html(
        """
        <div class="dp-prep">
        """
    )

    for transformation in transformations:

        st.html(
            f"""
            <div class="dp-transform">
                {transformation}
            </div>
            """
        )

    if preparation.get(
        "success",
        False,
    ):

        st.html(
            """
            <div class="dp-success">
                Dataset preparation completed successfully.
            </div>
            """
        )

    st.html(
        """
        </div>
        """
    )


# ============================================================
# PROCESSED DATASET
# ============================================================

if processed:

    render_section(
        "Processed Dataset",
        "Your prepared dataset is ready to download.",
    )

    filename = processed.get(
        "filename"
    )

    processed_rows = processed.get(
        "rows",
        0,
    )

    processed_columns = processed.get(
        "columns",
        0,
    )

    st.html(
        f"""
        <div class="dp-file">

            <div class="dp-file-label">
                Processed file
            </div>

            <div class="dp-file-name">
                {filename}
            </div>

        </div>
        """
    )

    d1, d2 = st.columns(2)

    with d1:

        st.metric(
            "Processed Rows",
            format_number(
                processed_rows
            ),
        )

    with d2:

        st.metric(
            "Processed Columns",
            format_number(
                processed_columns
            ),
        )

    if filename:

        try:

            download_response = requests.get(
                f"{API_URL}/api/v1/datasets/{filename}",
                timeout=30,
            )

            if download_response.status_code == 200:

                st.download_button(
                    "Download Processed Dataset",
                    data=download_response.content,
                    file_name=filename,
                    mime="text/csv",
                    use_container_width=True,
                )

            else:

                st.warning(
                    "Processed file could not be downloaded."
                )

        except requests.RequestException:

            st.warning(
                "Could not connect to the download endpoint."
            )


# ============================================================
# FOOTER
# ============================================================

st.html(
    """
    <div style="
        margin-top:60px;
        padding-top:20px;
        text-align:center;
        border-top:1px solid #e5e7eb;
        color:#777777;
        font-size:0.72rem;
    ">
        DataPilot AI · Automated Dataset Intelligence
    </div>
    """
)
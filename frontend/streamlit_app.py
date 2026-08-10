import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="DataPilot AI",
    page_icon="📊",
    layout="wide",
)


st.title("📊 DataPilot AI")
st.subheader("Autonomous Dataset Automation Agent")

st.write(
    "Upload a dataset to begin the DataPilot AI workflow."
)

st.divider()


# --------------------------------------------------
# Backend health
# --------------------------------------------------

st.subheader("Backend Status")

try:
    response = requests.get(
        f"{API_URL}/health",
        timeout=5,
    )

    if response.status_code == 200:
        st.success("Backend is online.")
    else:
        st.warning("Backend returned an unexpected response.")

except requests.RequestException:
    st.error(
        "Backend is offline. Start FastAPI with "
        "`uvicorn app.main:app --reload`."
    )


st.divider()


# --------------------------------------------------
# Dataset Upload
# --------------------------------------------------

st.subheader("Upload Dataset")

uploaded_file = st.file_uploader(
    "Choose a dataset",
    type=["csv", "xlsx", "xls", "json"],
    help="Supported formats: CSV, XLSX, XLS, JSON",
)


if uploaded_file is not None:

    st.write(
        f"**Selected file:** `{uploaded_file.name}`"
    )

    st.write(
        f"**Size:** {uploaded_file.size:,} bytes"
    )

    if st.button(
        "Upload Dataset",
        type="primary",
    ):

        with st.spinner("Uploading dataset..."):

            try:

                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type,
                    )
                }

                response = requests.post(
                    f"{API_URL}/dataset/upload",
                    files=files,
                    timeout=60,
                )

                if response.status_code == 200:

                    result = response.json()

                    st.success(
                        "Dataset uploaded successfully."
                    )

                    dataset = result["dataset"]

                    st.divider()

                    st.subheader(
                        "Dataset Information"
                    )

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric(
                            "Rows",
                            dataset["rows"],
                        )

                    with col2:
                        st.metric(
                            "Columns",
                            dataset["columns"],
                        )

                    with col3:
                        st.metric(
                            "File",
                            dataset["original_filename"],
                        )

                    st.write(
                        "**Stored filename:**",
                        dataset["stored_filename"],
                    )

                    st.write(
                        "**Columns:**"
                    )

                    st.write(
                        dataset["column_names"]
                    )

                else:

                    try:
                        error = response.json()
                        message = error.get(
                            "detail",
                            "Upload failed.",
                        )
                    except ValueError:
                        message = response.text

                    st.error(
                        f"Upload failed: {message}"
                    )

            except requests.RequestException as exc:

                st.error(
                    f"Could not connect to DataPilot backend: {exc}"
                )
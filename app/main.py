from fastapi import FastAPI, File, HTTPException, UploadFile

from app.api.analysis import router as analysis_router
from app.config import settings
from app.tools.file_loader import DatasetLoadError, load_dataset
from app.utils.file_utils import (
    ensure_directory,
    generate_unique_filename,
)
from app.utils.logger import get_logger, setup_logging


# --------------------------------------------------
# Logging
# --------------------------------------------------

setup_logging()

logger = get_logger(__name__)


# --------------------------------------------------
# FastAPI Application
# --------------------------------------------------

app = FastAPI(
    title=settings.app_name,
    description=(
        "AI-powered autonomous dataset analysis "
        "and automation platform."
    ),
    version="0.1.0",
)


# --------------------------------------------------
# API Routers
# --------------------------------------------------

app.include_router(analysis_router)


# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------

@app.get("/")
def root():
    """Return basic application information."""

    return {
        "name": settings.app_name,
        "version": "0.1.0",
        "status": "running",
    }


# --------------------------------------------------
# Health Endpoint
# --------------------------------------------------

@app.get("/health")
def health():
    """Return application health status."""

    return {
        "status": "healthy",
    }


# --------------------------------------------------
# Dataset Upload Endpoint
# --------------------------------------------------

@app.post("/dataset/upload")
async def upload_dataset(
    file: UploadFile = File(...),
):
    """
    Upload a dataset, validate it, save it to raw storage,
    and verify that it can be loaded into pandas.
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required.",
        )

    raw_directory = ensure_directory(
        settings.project_root / settings.raw_data_dir
    )

    unique_filename = generate_unique_filename(
        file.filename
    )

    destination = raw_directory / unique_filename

    logger.info(
        "Receiving dataset upload: %s",
        file.filename,
    )

    try:
        # ------------------------------------------
        # Read uploaded file
        # ------------------------------------------

        contents = await file.read()

        if not contents:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty.",
            )

        # ------------------------------------------
        # File size validation
        # ------------------------------------------

        if len(contents) > settings.max_file_size_bytes:
            raise HTTPException(
                status_code=413,
                detail=(
                    f"File exceeds the maximum allowed size of "
                    f"{settings.max_file_size_mb} MB."
                ),
            )

        # ------------------------------------------
        # Save file
        # ------------------------------------------

        destination.write_bytes(contents)

        # ------------------------------------------
        # Verify dataset can be loaded
        # ------------------------------------------

        dataframe = load_dataset(destination)

        logger.info(
            "Dataset upload successful: %s",
            unique_filename,
        )

        # ------------------------------------------
        # Response
        # ------------------------------------------

        return {
            "success": True,
            "dataset": {
                "original_filename": file.filename,
                "stored_filename": unique_filename,
                "path": str(destination),
                "rows": len(dataframe),
                "columns": len(dataframe.columns),
                "column_names": dataframe.columns.tolist(),
            },
        }

    except HTTPException:
        # Remove partially processed file.
        if destination.exists():
            destination.unlink()

        raise

    except DatasetLoadError as exc:
        # Remove invalid dataset.
        if destination.exists():
            destination.unlink()

        logger.error(
            "Dataset loading failed: %s",
            exc,
        )

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        # Remove file after unexpected failure.
        if destination.exists():
            destination.unlink()

        logger.exception(
            "Unexpected dataset upload failure."
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unexpected error while processing "
                "the dataset."
            ),
        ) from exc
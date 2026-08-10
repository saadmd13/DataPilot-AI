from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile

from app.config import settings
from app.tools.file_loader import DatasetLoadError, load_dataset
from app.utils.file_utils import (
    generate_unique_filename,
    ensure_directory,
)
from app.utils.logger import get_logger, setup_logging


setup_logging()

logger = get_logger(__name__)

app = FastAPI(
    title=settings.app_name,
    description="AI-powered autonomous dataset analysis and automation platform.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "name": settings.app_name,
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


@app.post("/dataset/upload")
async def upload_dataset(file: UploadFile = File(...)):
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

    unique_filename = generate_unique_filename(file.filename)

    destination = raw_directory / unique_filename

    logger.info(
        "Receiving dataset upload: %s",
        file.filename,
    )

    try:
        contents = await file.read()

        if not contents:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty.",
            )

        if len(contents) > settings.max_file_size_bytes:
            raise HTTPException(
                status_code=413,
                detail=(
                    f"File exceeds the maximum allowed size of "
                    f"{settings.max_file_size_mb} MB."
                ),
            )

        destination.write_bytes(contents)

        dataframe = load_dataset(destination)

        logger.info(
            "Dataset upload successful: %s",
            unique_filename,
        )

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
        if destination.exists():
            destination.unlink()
        raise

    except DatasetLoadError as exc:
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
        if destination.exists():
            destination.unlink()

        logger.exception(
            "Unexpected dataset upload failure."
        )

        raise HTTPException(
            status_code=500,
            detail="Unexpected error while processing the dataset.",
        ) from exc
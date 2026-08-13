import sys
import json
from pathlib import Path

from app.services.analysis_pipeline import DataPilotAnalyzer
from app.tools.file_loader import load_dataset


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python test_analysis.py <path_to_csv>")
        print()
        print("Example:")
        print(r"  python test_analysis.py data\pulsar.csv")
        return

    dataset_path = Path(sys.argv[1])

    if not dataset_path.exists():
        print(f"ERROR: Dataset not found: {dataset_path}")
        return

    print("=" * 70)
    print("DataPilot AI - Full Dataset Analysis")
    print("=" * 70)
    print(f"Dataset: {dataset_path}")
    print()

    try:
        dataframe = load_dataset(dataset_path)

        print(
            f"Loaded: {len(dataframe):,} rows x "
            f"{len(dataframe.columns)} columns"
        )
        print()

        analyzer = DataPilotAnalyzer()

        result = analyzer.analyze(
            dataframe=dataframe,
            filename=dataset_path.name,
        )

        print(json.dumps(
            result.model_dump(),
            indent=2,
            default=str,
        ))

    except Exception as exc:
        print(f"ERROR: {exc}")
        raise


if __name__ == "__main__":
    main()
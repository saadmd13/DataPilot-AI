import pandas as pd

from app.services.data_preparation_pipeline import (
    DataPreparationPipeline,
)


def main() -> None:
    dataframe = pd.DataFrame(
        {
            "customer_id": [1, 2, 3, 3, 4, 5, 6, 7],
            "age": [25, None, 30, 30, None, 40, 35, None],
            "city": [
                "Delhi",
                "Mumbai",
                None,
                None,
                "Delhi",
                "Delhi",
                "Mumbai",
                "Delhi",
            ],
            "country": [
                "India",
                "India",
                "India",
                "India",
                "India",
                "India",
                "India",
                "India",
            ],
            "salary": [
                30000,
                45000,
                50000,
                50000,
                55000,
                None,
                60000,
                65000,
            ],
        }
    )

    print("=" * 70)
    print("BEFORE DATA PREPARATION")
    print("=" * 70)

    print(f"Rows: {len(dataframe)}")
    print(f"Columns: {len(dataframe.columns)}")
    print(
        f"Missing cells: {int(dataframe.isna().sum().sum())}"
    )
    print(
        f"Missing percentage: "
        f"{dataframe.isna().mean().mean() * 100:.2f}%"
    )
    print(
        f"Duplicate rows: "
        f"{int(dataframe.duplicated().sum())}"
    )

    print("\nColumns:")
    print(dataframe.columns.tolist())

    print("\nMissing values:")
    print(dataframe.isna().sum())

    pipeline = DataPreparationPipeline()

    prepared, result = pipeline.prepare(
        dataframe,
        filename="messy_test_dataset.csv",
    )

    print("\n" + "=" * 70)
    print("TRANSFORMATIONS APPLIED")
    print("=" * 70)

    for transformation in result.transformations:
        print(f"- {transformation}")

    print("\n" + "=" * 70)
    print("AFTER DATA PREPARATION")
    print("=" * 70)

    print(f"Rows: {len(prepared)}")
    print(f"Columns: {len(prepared.columns)}")
    print(
        f"Missing cells: "
        f"{int(prepared.isna().sum().sum())}"
    )
    print(
        f"Missing percentage: "
        f"{prepared.isna().mean().mean() * 100:.2f}%"
    )
    print(
        f"Duplicate rows: "
        f"{int(prepared.duplicated().sum())}"
    )

    print("\nColumns:")
    print(prepared.columns.tolist())

    print("\nPrepared dataset:")
    print(prepared)

    print("\n" + "=" * 70)
    print("TRANSFORMATION SUMMARY")
    print("=" * 70)

    print(
        f"Rows: "
        f"{result.original_row_count} → "
        f"{result.final_row_count}"
    )

    print(
        f"Columns: "
        f"{result.original_column_count} → "
        f"{result.final_column_count}"
    )

    print(
        f"Missing: "
        f"{result.original_missing_percentage:.2f}% → "
        f"{result.final_missing_percentage:.2f}%"
    )

    print(
        f"Transformations applied: "
        f"{result.transformations_applied}"
    )

    print(f"Success: {result.success}")
    print(f"Message: {result.message}")


if __name__ == "__main__":
    main()
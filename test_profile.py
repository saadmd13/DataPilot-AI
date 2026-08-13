import pandas as pd

from app.services.dataset_profiler import DatasetProfiler


dataframe = pd.DataFrame(
    {
        "customer_id": list(range(1, 101)),

        "name": [
            f"Customer {i}"
            for i in range(1, 101)
        ],

        "age": [
            20 + (i % 30)
            for i in range(100)
        ],

        "city": [
            [
                "Hyderabad",
                "Mumbai",
                "Delhi",
                "Bangalore",
            ][i % 4]
            for i in range(100)
        ],

        "active": [
            i % 2 == 0
            for i in range(100)
        ],

        "signup_date": [
            f"2026-01-{(i % 28) + 1:02d}"
            for i in range(100)
        ],

        "email": [
            f"customer{i}@example.com"
            for i in range(1, 101)
        ],

        "phone": [
            f"+9198765432{i:02d}"
            for i in range(100)
        ],
        
        "website": [
            "https://example.com"
            for _ in range(100)
        ],
    }
)


profiler = DatasetProfiler()


profile = profiler.profile(
    dataframe,
    filename="test_dataset.csv",
)


print(
    profile.model_dump_json(
        indent=2
    )
)
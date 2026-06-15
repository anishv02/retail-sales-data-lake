import pandas as pd
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from validation.validator import (
    SalesValidator
)

from validation.audit import (
    generate_audit
)

df = pd.read_csv(
    "data/source/retail_sales.csv"
)

validator = SalesValidator(df)

valid_df, invalid_df, validation_report = (
    validator.execute()
)

audit = generate_audit(
    len(df),
    len(valid_df),
    len(invalid_df)
)

print("\nAUDIT")
print(audit)

print("\nVALIDATION REPORT")
print(validation_report)

print("\nVALID RECORDS")
print(valid_df)

print("\nINVALID RECORDS")
print(invalid_df)
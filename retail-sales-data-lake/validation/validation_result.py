import pandas as pd 

from validation.validator import SalesValidator 
from dataclasses import dataclass


@dataclass
class ValidationResult:
    records_read: int
    records_passed: int
    records_failed: int
    validation_name: str

df = pd.read_csv(
    "data/source/retail_sales.csv"
)

validator = SalesValidator(df)  

valid_df, invalid_df = (
    validator.validatte_mandatory_fields()
) 

print("\nVALID RECORDS")
print(valid_df)

print("\nINVALID RECORDS")
print(invalid_df)


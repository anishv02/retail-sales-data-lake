import pandas as pd 

from validation.validation_rules import (
    MANDATORY_COLUMNS
)
from validation.rules import (
    VALIDATION_RULES
)

class SalesValidator : 
    def __init__(self, df):
        self.df = df.copy()
        self.validation_errors = []

    def execute(self):
        for rule in VALIDATION_RULES:
            if rule["rule_type"] == "mandatory":
                mask = (
                    self.df[rule["column"]]
                    .isnull()
                )
            elif rule["rule_type"] == "positive":
                mask = (
                    self.df[rule["column"]].isnull()
                    |
                    (self.df[rule["column"]] <= 0)
                )
            elif rule["rule_type"] == "date":
                parsed_dates = pd.to_datetime(
                    self.df[rule["column"]],
                    errors="coerce"
                )
                mask = parsed_dates.isnull()
            elif rule["rule_type"] == "duplicate":
                mask = self.df.duplicated(
                    subset=[rule["column"]],
                    keep=False
                )
            else:
                continue

            failed_rows = self.df[mask]

            for index, row in failed_rows.iterrows():
                self.validation_errors.append({
                    "row_index": index,
                    "order_id": row["order_id"],
                    "rule_name": rule["rule_name"],
                    "error_message": rule["error_message"]
                })

        validation_report = pd.DataFrame(self.validation_errors)

        invalid_orders = set()
        if not validation_report.empty and "order_id" in validation_report.columns:
            invalid_orders = set(validation_report["order_id"])

        valid_df = self.df[~self.df["order_id"].isin(invalid_orders)]
        invalid_df = self.df[self.df["order_id"].isin(invalid_orders)]

        return (
            valid_df,
            invalid_df,
            validation_report
        )
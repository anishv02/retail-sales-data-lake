import pandas as pd


def create_validation_report(
        validation_errors
):

    return pd.DataFrame(
        validation_errors
    )
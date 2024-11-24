from typing import List
import pandas as pd
from databricks.feature_store import FeatureStoreClient

def push_value_to_feature_table(
    value: dict,
    feature_table_name: str,
    feature_table_primary_keys: List[str],
    feature_table_event_time: str,
):
    """
    Pushes the given `value` to the given `feature_table_name` in the Databricks Feature Store.

    Args:
        value (dict): The value to push to the Feature Store
        feature_table_name (str): The name of the Feature Table
        feature_table_primary_keys (List[str]): The primary keys of the Feature Table
        feature_table_event_time (str): The event time column of the Feature Table

    Returns:
        None
    """
    # Initialize the Feature Store client
    fs = FeatureStoreClient()

    # Transform the value dictionary into a pandas DataFrame
    value_df = pd.DataFrame([value])

    # Get or create the feature table in the Feature Store
    try:
        # Check if the feature table exists (assuming prior schema setup)
        feature_table = fs.get_feature_table(name=feature_table_name)
    except Exception as e:
        # If it doesn't exist, create the feature table
        schema = (
            value_df.dtypes.reset_index()
            .rename(columns={"index": "column_name", 0: "data_type"})
            .to_dict(orient="records")
        )
        feature_table = fs.create_feature_table(
            name=feature_table_name,
            keys=feature_table_primary_keys,
            timestamp_keys=[feature_table_event_time],
            schema=schema,
            description=f"Feature Table for {feature_table_name}",
        )

    # Insert the value DataFrame into the Feature Store
    fs.write_table(name=feature_table_name, df=value_df, mode="merge")

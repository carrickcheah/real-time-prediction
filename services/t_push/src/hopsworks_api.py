from typing import List

import hopsworks
import hsfs
import pandas as pd

from src.config import hopsworks_config as config

def push_value_to_feature_group(
    value: dict,
    feature_group_name: str,
    feature_group_version: int,
    feature_group_primary_keys: List[str],
    feature_group_event_time: str,
):
    """
    Pushes the given `value` to the given `feature_group_name` in the Feature Store.

    Args:
        value (dict): The value to push to the Feature Store
        feature_group_name (str): The name of the Feature Group
        feature_group_version (int): The version of the Feature Group
        feature_group_primary_keys (List[str]): The primary key of the Feature Group
        feature_group_event_time (str): The event time of the Feature Group

    Returns:
        None
    """

    
    project = hopsworks.login(
        project=config.hopsworks_project_name,
        api_key=config.hopsworks_api_key,
    )

    feature_store = project.get_feature_store()

    feature_group = feature_store.get_or_create_feature_group(
        name=feature_group_name,
        version=feature_group_version,
        primary_key=feature_group_primary_keys,
        event_time=feature_group_event_time,
        online_enabled=True,

        # TODO: either as homework or I will show one example.
        # expectation_suite=expectation_suite_transactions,
    )

    # transform the value dict into a pandas DataFrame
    value_df = pd.DataFrame([value])

    # push the value to the Feature Store
    feature_group.insert(value_df)




# from typing import List
# import hsfs  # change here: switched to using hsfs for feature store interactions
# import pandas as pd

# from src.config import hopsworks_config as config

# def push_value_to_feature_group(
#     value: dict,
#     feature_group_name: str,
#     feature_group_version: int,
#     feature_group_primary_keys: List[str],
#     feature_group_event_time: str,
# ):
#     """
#     Pushes the given `value` to the given `feature_group_name` in the Feature Store.

#     Args:
#         value (dict): The value to push to the Feature Store
#         feature_group_name (str): The name of the Feature Group
#         feature_group_version (int): The version of the Feature Group
#         feature_group_primary_keys (List[str]): The primary keys of the Feature Group
#         feature_group_event_time (str): The event time column of the Feature Group

#     Returns:
#         None
#     """
#     # Establish a connection to the Hopsworks Feature Store
#     connection = hsfs.connection(  # change here: switched from hopsworks.login to hsfs.connection
#         host=config.hopsworks_host,  # change here: added `host` parameter for hsfs connection
#         project=config.hopsworks_project_name,
#         api_key=config.hopsworks_api_key
#     )
#     feature_store = connection.get_feature_store()  # change here: switched to `connection.get_feature_store()`

#     # Retrieve or create the feature group
#     try:
#         # Attempt to retrieve the existing feature group
#         feature_group = feature_store.get_feature_group(  # change here: switched to `get_feature_group` from hsfs
#             name=feature_group_name, version=feature_group_version
#         )
#     except Exception:
#         # Create the feature group if it doesn't exist
#         feature_group = feature_store.create_feature_group(  # change here: replaced `get_or_create_feature_group` with `create_feature_group`
#             name=feature_group_name,
#             version=feature_group_version,
#             primary_key=feature_group_primary_keys,
#             event_time=feature_group_event_time,
#             online_enabled=True,
#             description=f"Feature Group: {feature_group_name}"  # change here: added a description parameter
#         )

#     # Transform the value dictionary into a pandas DataFrame
#     value_df = pd.DataFrame([value])

#     # Insert the DataFrame into the Feature Store
#     feature_group.insert(value_df)  # change here: insert remains compatible with hsfs




from src.config import CometConfig, HopsworksConfig
from src.feature_engineering import add_technical_indicators_and_temporal_features
from src.models.current_price_baseline import CurrentPriceBaseline
from src.models.xgboost_model import XGBoostModel
from src.utils import hash_dataframe
from src.model_registry import get_model_name
from src.preprocessing import keep_only_numeric_columns

def train_model(
    comet_config: CometConfig,
    hopsworks_config: HopsworksConfig,
    feature_view_name: str,
    feature_view_version: int,
    feature_group_name: str,
    feature_group_version: int,
    ohlc_window_sec: int,
    product_id: str,
    last_n_days: int,
    forecast_steps: int,
    perc_test_data: Optional[float] = 0.3,
    n_search_trials: Optional[int] = 10,
    n_splits: Optional[int] = 3,
    last_n_minutes: Optional[int] = 30,
):
    
    """
    Read feature from feature store, 
    train a model and save it in the model registry.

    Args:
        comet_config: Configuration for Comet.ml
        hopsworks_config: Configuration for Hopsworks
        feature_view_name: Name of the feature view to read from the feature store
        feature_view_version: Version of the feature view to read from the feature store
        feature_group_name: Name of the feature group to read from the feature store
        feature_group_version: Version of the feature group to read from the feature store
        ohlc_window_sec: Window size for the OHLC data
        product_id: Product ID to read from the feature store
        last_n_days: Number of days to read from the feature store
        forecast_steps: Number of steps to forecast
        perc_test_data: Percentage of test data
        n_search_trials: Number of search trials for hyperparameter optimization
        n_splits: Number of splits for cross-validation
        last_n_minutes: Number of minutes to read from the feature
        
    Returns:
        None
    """

    # Load feature from feature store
    from src.ohlc_data_reader import OhlcDataReader

    ohlc_data_reader = OhlcDataReader(
        feature_view_name=feature_view_name,
        feature_view_version=feature_view_version,
        feature_group_name=feature_group_name,
        feature_group_version=feature_group_version,
        ohlc_window_sec=ohlc_window_sec,
    )

    ohlc_data = ohlc_data_reader.read_from_offline_store(
          product_id=product_id,
          last_n_days=last_n_days,
          
    )

    # split the data into train and test set


    # Add column to the target price we want to predict
    ohlc_data['target_price'] = ohlc_data['close'].shift(-forecast_steps)




    # Build model

    # Push model to model registry




# Entry point of the application

if __name__ == "__main__":
        
        from src.config import config, HopsworksConfig

        train_model(
            comet_config=config.comet,
            hopsworks_config=config.hopsworks,
            feature_view_name=config.feature_view_name,
            feature_view_version=config.feature_view_version,
            feature_group_name=config.feature_group_name,   
            feature_group_version=config.feature_group_version,
            ohlc_window_sec=config.ohlc_window_sec,
            product_id=config.product_id,
            last_n_days=config.last_n_days,


        )




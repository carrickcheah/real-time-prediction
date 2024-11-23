from src.config import config
from datetime import timedelta
from quixstreams import Application
from loguru import logger


def init_ohlcv_candle(trade: dict):
    """
    Returns the initial OHLCV candle when the first `trade` in that window happens.

    Args:
        trade (dict): Trade data.

    Returns:
        dict: Initial OHLCV candle.
    """

    return {
        'open': trade['price'],
        'high': trade['price'],
        'low': trade['price'],
        'close': trade['price'],
        'volume': trade['quantity'],
        # 'timestamp_ms': None,
    }



def update_ohlcv_candle(
        candle: dict, 
        trade: dict
):
    
    """
    Updates the OHLCV candle with the new `trade`.

    Args:
        candle (dict): OHLCV candle.
        trade (dict): Trade data.   

    Returns:
        dict: Updated OHLCV candle.

    """
    candle['high'] = max(candle['high'], trade['price'])
    candle['low'] = min(candle['low'], trade['price'])
    candle['close'] = trade['price']
    candle['volume'] += trade['quantity']
    # candle['timestamp_ms'] = trade['timestamp_ms']

    return candle



def transform_trade_to_ohlc(
        kafka_broker_address : str,
        kafka_input_topic : str,
        kafka_output_topic : str,
        kafka_consumer_group : str,
        ohlcv_window_seconds : int
):
    
    """
    Read data from kafka_input_topic, 
    transform OHLCV data and 
    write it to kafka_output_topic.

    Args:
        kafka_broker_address (str): Kafka broker address.
        kafka_input_topic (str): Kafka topic to read data from.
        kafka_output_topic (str): Kafka topic to write data to.
        kafka_consumer_group (str): Kafka consumer group.
        ohlcv_window_seconds (int): OHLCV window in seconds.

    Returns:
        None

    """
    # Create a new application
    app = Application(
        broker_address=kafka_broker_address,
        consumer_group=kafka_consumer_group,
    )


    # Define the input and output topics, and their value deserializer and serializer, respectively.
    # The value deserializer is used to deserialize the message value when reading from the input topic.
    # The value serializer is used to serialize the message value when writing to the output topic.
    input_topic = app.topic(name=kafka_input_topic, value_deserializer='json')
    output_topic = app.topic(name=kafka_output_topic, value_serializer='json')


    # create a streaming dataframes from the input topic
    sdf = app.dataframe(input_topic)

    # check if we are actually reading incoming trades
    # sdf.update(logger.debug)

    # create a tumbling window of trades, and reduce them to OHLCV candles, and write them to the output topic.
    # reducer is a function that takes two arguments: the current value of the accumulator and the new value to be added.
    # The `initializer` argument is used to initialize the OHLCV candle when the first trade in that window happens.
    # The `final` method is used to get the final result of the computation.
    # The `current` method is used to get the current result of the computation.
    # The `duration_ms` argument is used to specify the duration of the window in milliseconds.
    sdf = (
        sdf.tumbling_window(duration_ms=timedelta(seconds=ohlcv_window_seconds))
        .reduce(reducer=update_ohlcv_candle, initializer=init_ohlcv_candle)
        .final()
        # .current()
    )   

    # unpack the dictionary into separate columns
    sdf['open'] = sdf['value']['open']
    sdf['high'] = sdf['value']['high']
    sdf['low'] = sdf['value']['low']
    sdf['close'] = sdf['value']['close']
    sdf['volume'] = sdf['value']['volume']
    sdf['timestamp_ms'] = sdf['end']

    # print the output to the console
    sdf.update(logger.debug)

    # push these message to the output topic
    sdf = sdf.to_topic(output_topic)

    # kick off the application
    app.run(sdf)



# Entry point of the application
if __name__ == "__main__":

    transform_trade_to_ohlc(
        kafka_broker_address=config.kafka_broker_address,
        kafka_input_topic=config.kafka_input_topic,
        kafka_output_topic=config.kafka_output_topic,
        kafka_consumer_group=config.kafka_consumer_group,
        ohlcv_window_seconds=config.ohlcv_window_seconds
    )
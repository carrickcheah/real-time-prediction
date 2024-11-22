from typing import List
from loguru import logger
from quixstreams import Application
from src.kraken_websocket_api import ( KrakenWebsocketAPI,Trade )
from src.config import config

# create a new ingest service
def t_ingest(
    kafka_broker_address: str,
    kafka_topic: str,
    product_id: str,
):
    """"
    Read data from Kraken websocket and ingest it into kafka_topic.

    Args:
        kafka_broker_address (str): Kafka broker address.
        kafka_topic (str): Kafka topic to ingest data into.
        product_id (str): btc/usd    

    """


     # Create an Application instance with Kafka config
    app = Application(broker_address=kafka_broker_address)

    # Define a topic "my_topic" with JSON serialization
    topic = app.topic(name=kafka_topic, value_serializer='json')

    # create a kraken api object
    kraken_api = KrakenWebsocketAPI(product_id=product_id)

    # Create a Producer instance
    with app.get_producer() as producer:

        while True:

            trades: List[Trade] = kraken_api.get_trades()
            
            for trade in trades:
                # Serialize an event using the defined Topic
                # transform it into a sequence of bytes
                message = topic.serialize(key=trade.product_id, value=trade.model_dump())
                
                # Produce a message into the Kafka topic
                producer.produce(topic=topic.name, value=message.value, key=message.key)

                logger.debug(f"Pushed trade to Kafka: {trade}")




# Entry point of the application
if __name__ == "__main__":

    t_ingest(
        kafka_broker_address=config.kafka_broker_address,
        kafka_topic=config.kafka_topic,
        product_id=config.product_id,   
    )
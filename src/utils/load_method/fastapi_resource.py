from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from kafka import KafkaConsumer,KafkaProducer
from time import sleep
import json
from sqlalchemy import create_engine

from src.utils.load_method.load_utils import register_load_method
from src.utils.load_method.common_resource import load_json


@register_load_method
def fastapi_app() -> FastAPI:
    app = FastAPI(
        title="Internal tool",
        description="FastAPI server for Account Interaction.",
        version="1.0.0"
    )
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        openapi_schema = get_openapi(
            title="Internal tool",
            version="1.0.0",
            description="FastAPI server for Account Interaction.",
            routes=app.routes,
        )
        app.openapi_schema = openapi_schema
        return app.openapi_schema
    app.openapi = custom_openapi
    
    return app



@register_load_method
def kafka_producer():
    class MessageProducer:
        broker = ""
        topic = ""
        producer = None
        def __init__(self, broker, topic):
            self.broker = broker
            self.topic = topic
            self.producer = KafkaProducer(bootstrap_servers=self.broker,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks='all',
            retries = 3)


        def send_msg(self, msg):
            print("sending message...")
            try:
                future = self.producer.send(self.topic,msg)
                self.producer.flush()
                future.get(timeout=60)
                print("message sent successfully...")
                return {'status_code':200, 'error':None}
            except Exception as ex:
                return ex
    broker = 'localhost:9092'
    topic = 'handle-topic'
    producer = MessageProducer(broker,topic)
    return producer
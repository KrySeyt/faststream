from docs.docs_src.getting_started.asyncapi.asyncapi_customization.custom_broker import app, docs_obj
from faststream.specification.asyncapi import AsyncAPI


def test_broker_customization():
    schema = docs_obj.jsonable()

    assert schema["servers"] == {
        "development": {
            "url": "non-sensitive-url:9092",
            "protocol": "kafka",
            "description": "Kafka broker running locally",
            "protocolVersion": "auto",
        }
    }

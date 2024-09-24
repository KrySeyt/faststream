from faststream.nats import NatsBroker
from faststream.specification.asyncapi import AsyncAPI


def test_kv_schema():
    broker = NatsBroker()

    @broker.subscriber("test", kv_watch="test")
    async def handle(): ...

    schema = AsyncAPI(broker, schema_version="3.0.0").jsonable()

    assert schema["channels"] == {}

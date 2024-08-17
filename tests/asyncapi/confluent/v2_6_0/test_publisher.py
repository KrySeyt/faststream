from faststream.specification.asyncapi.generate import get_app_schema
from faststream.confluent import KafkaBroker
from faststream.specification.asyncapi.version import AsyncAPIVersion
from tests.asyncapi.base.v2_6_0.publisher import PublisherTestcase


class TestArguments(PublisherTestcase):
    broker_class = KafkaBroker

    def test_publisher_bindings(self):
        broker = self.broker_class()

        @broker.publisher("test")
        async def handle(msg): ...

        schema = get_app_schema(self.build_app(broker), version=AsyncAPIVersion.v2_6).to_jsonable()
        key = tuple(schema["channels"].keys())[0]  # noqa: RUF015

        assert schema["channels"][key]["bindings"] == {
            "kafka": {"bindingVersion": "0.4.0", "topic": "test"}
        }

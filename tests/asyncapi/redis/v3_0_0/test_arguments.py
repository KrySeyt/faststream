from faststream.specification.asyncapi.generate import get_app_schema
from faststream.redis import RedisBroker, StreamSub
from faststream.specification.asyncapi.version import AsyncAPIVersion
from tests.asyncapi.base.v3_0_0.arguments import ArgumentsTestcase


class TestArguments(ArgumentsTestcase):
    broker_factory = RedisBroker

    def test_channel_subscriber(self):
        broker = self.broker_factory()

        @broker.subscriber("test")
        async def handle(msg): ...

        schema = get_app_schema(self.build_app(broker), version=AsyncAPIVersion.v3_0).to_jsonable()
        key = tuple(schema["channels"].keys())[0]  # noqa: RUF015

        assert schema["channels"][key]["bindings"] == {
            "redis": {
                "bindingVersion": "custom",
                "channel": "test",
                "method": "subscribe",
            }
        }

    def test_channel_pattern_subscriber(self):
        broker = self.broker_factory()

        @broker.subscriber("test.{path}")
        async def handle(msg): ...

        schema = get_app_schema(self.build_app(broker), version=AsyncAPIVersion.v3_0).to_jsonable()
        key = tuple(schema["channels"].keys())[0]  # noqa: RUF015

        assert schema["channels"][key]["bindings"] == {
            "redis": {
                "bindingVersion": "custom",
                "channel": "test.*",
                "method": "psubscribe",
            }
        }

    def test_list_subscriber(self):
        broker = self.broker_factory()

        @broker.subscriber(list="test")
        async def handle(msg): ...

        schema = get_app_schema(self.build_app(broker), version=AsyncAPIVersion.v3_0).to_jsonable()
        key = tuple(schema["channels"].keys())[0]  # noqa: RUF015

        assert schema["channels"][key]["bindings"] == {
            "redis": {"bindingVersion": "custom", "channel": "test", "method": "lpop"}
        }

    def test_stream_subscriber(self):
        broker = self.broker_factory()

        @broker.subscriber(stream="test")
        async def handle(msg): ...

        schema = get_app_schema(self.build_app(broker), version=AsyncAPIVersion.v3_0).to_jsonable()
        key = tuple(schema["channels"].keys())[0]  # noqa: RUF015

        assert schema["channels"][key]["bindings"] == {
            "redis": {"bindingVersion": "custom", "channel": "test", "method": "xread"}
        }

    def test_stream_group_subscriber(self):
        broker = self.broker_factory()

        @broker.subscriber(stream=StreamSub("test", group="group", consumer="consumer"))
        async def handle(msg): ...

        schema = get_app_schema(self.build_app(broker), version=AsyncAPIVersion.v3_0).to_jsonable()
        key = tuple(schema["channels"].keys())[0]  # noqa: RUF015

        assert schema["channels"][key]["bindings"] == {
            "redis": {
                "bindingVersion": "custom",
                "channel": "test",
                "consumer_name": "consumer",
                "group_name": "group",
                "method": "xreadgroup",
            }
        }

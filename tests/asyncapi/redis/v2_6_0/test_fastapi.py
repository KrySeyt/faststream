from typing import Type

from faststream.redis import TestRedisBroker
from faststream.redis.fastapi import RedisRouter
from tests.asyncapi.base.v2_6_0.arguments import FastAPICompatible
from tests.asyncapi.base.v2_6_0.fastapi import FastAPITestCase
from tests.asyncapi.base.v2_6_0.publisher import PublisherTestcase


class TestRouterArguments(FastAPITestCase, FastAPICompatible):
    broker_class: Type[RedisRouter] = RedisRouter
    broker_wrapper = staticmethod(TestRedisBroker)

    def build_app(self, router):
        return router


class TestRouterPublisher(PublisherTestcase):
    broker_class = RedisRouter

    def build_app(self, router):
        return router

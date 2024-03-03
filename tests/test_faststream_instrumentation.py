from unittest import TestCase

import wrapt
from faststream_instrumentation import FastStreamInstrumentator
from faststream import FastStream
from faststream.redis.broker import RedisBroker
from faststream.redis.producer import RedisFastProducer

class TestFastStream(TestCase):
    def test_instrument_api(self) -> None:
        app = FastStream(broker=RedisBroker())
        FastStreamInstrumentator.instrument_app(app)
        self.assertTrue(isinstance(RedisBroker._process_message, wrapt.BoundFunctionWrapper))
        self.assertTrue(
            isinstance(RedisFastProducer.publish, wrapt.BoundFunctionWrapper)
        )
        FastStreamInstrumentator.uninstrument_app(app)
        self.assertFalse(isinstance(RedisBroker._process_message, wrapt.BoundFunctionWrapper))
        self.assertFalse(
            isinstance(RedisFastProducer.publish, wrapt.BoundFunctionWrapper)
        )
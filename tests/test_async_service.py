import unittest
import asyncio
from ai_core.service_api import async_call_asr

class TestAsyncService(unittest.IsolatedAsyncioTestCase):
    async def test_async_call_asr(self):
        text = await async_call_asr('none.wav', url='http://localhost:9')
        self.assertEqual(text, 'none')

if __name__ == '__main__':
    unittest.main()

import unittest
import os
from ai_core.service_api import (
    call_asr,
    call_tts,
    call_llm,
    call_voiceprint,
    call_memory_save,
    call_memory_query,
)


class TestServiceClients(unittest.TestCase):
    def test_fallbacks(self):
        bad_url = "http://localhost:9/notfound"
        self.assertEqual(call_asr("audio.wav", url=bad_url), "audio")
        self.assertEqual(call_voiceprint("user1.wav", url=bad_url), "user1")
        self.assertEqual(call_llm("hi", url=bad_url), "")
        self.assertEqual(call_tts("hello", url=bad_url), "")
        tmp = "tmp_memory.json"
        if os.path.exists(tmp):
            os.remove(tmp)
        self.assertFalse(os.path.exists(tmp))
        self.assertFalse(call_memory_save({"text": "hi"}, url=bad_url, fallback_path=tmp))
        self.assertTrue(os.path.exists(tmp))
        res = call_memory_query("hi", url=bad_url, fallback_path=tmp)
        self.assertIsInstance(res, list)
        os.remove(tmp)


if __name__ == "__main__":
    unittest.main()

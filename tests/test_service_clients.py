import unittest
from ai_core.service_clients import (
    call_asr,
    call_tts,
    call_llm,
    call_voiceprint,
)


class TestServiceClients(unittest.TestCase):
    def test_fallbacks(self):
        bad_url = "http://localhost:9/notfound"
        self.assertEqual(call_asr("audio.wav", url=bad_url), "audio")
        self.assertEqual(call_voiceprint("user1.wav", url=bad_url), "user1")
        self.assertEqual(call_llm("hi", url=bad_url), "")
        self.assertEqual(call_tts("hello", url=bad_url), "")


if __name__ == "__main__":
    unittest.main()

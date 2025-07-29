import unittest
from ai_core import IntelligentCore, UserInput

class TestIntelligentCore(unittest.TestCase):
    def test_process(self):
        core = IntelligentCore()
        user = UserInput(audio_path='voice.wav', image_path='face.png', text='Hi')
        reply = core.process(user)
        self.assertIsInstance(reply, str)
        self.assertIn('Hi', reply)

if __name__ == '__main__':
    unittest.main()

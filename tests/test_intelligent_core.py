import unittest
from ai_core import IntelligentCore, UserInput, reset, global_state

class TestIntelligentCore(unittest.TestCase):
    def test_process(self):
        reset()
        core = IntelligentCore()
        user = UserInput(audio_path='user1.wav', image_path='face.png', text='Hi')
        reply = core.process(user)
        self.assertIsInstance(reply.text, str)
        self.assertEqual(global_state.INTERACTION_COUNT, 1)

if __name__ == '__main__':
    unittest.main()

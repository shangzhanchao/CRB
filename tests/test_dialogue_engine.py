import unittest
from ai_core import DialogueEngine, reset

class TestDialogueEngine(unittest.TestCase):
    def test_generate_response(self):
        reset()
        engine = DialogueEngine()
        text = 'Hello'
        resp = engine.generate_response(text, 'happy', user_id='user1', touched=True)
        self.assertIsInstance(resp.text, str)
        self.assertIsInstance(resp.action, list)
        self.assertIn('hug', resp.action)
        self.assertGreater(len(engine.memory.records), 0)

if __name__ == '__main__':
    unittest.main()

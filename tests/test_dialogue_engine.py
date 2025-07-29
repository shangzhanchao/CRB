import unittest
from ai_core import DialogueEngine

class TestDialogueEngine(unittest.TestCase):
    def test_generate_response(self):
        engine = DialogueEngine()
        text = 'Hello'
        resp = engine.generate_response(text, 'praise')
        self.assertIn('You said: Hello', resp)
        self.assertGreater(len(engine.memory.records), 0)

if __name__ == '__main__':
    unittest.main()

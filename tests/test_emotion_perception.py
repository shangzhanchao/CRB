import unittest
from ai_core import EmotionPerception

class TestEmotionPerception(unittest.TestCase):
    def test_perceive(self):
        ep = EmotionPerception()
        state = ep.perceive('voice.wav', 'face.png')
        self.assertEqual(state.overall(), 'neutral')

if __name__ == '__main__':
    unittest.main()

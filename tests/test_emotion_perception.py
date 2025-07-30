import unittest
from ai_core import EmotionPerception

class TestEmotionPerception(unittest.TestCase):
    def test_perceive(self):
        ep = EmotionPerception()
        state = ep.perceive('voice.wav', 'face.png')
        self.assertEqual(state.overall(), 'neutral')
        uid = ep.recognize_identity('user1.wav')
        self.assertEqual(uid, 'user1')

    def test_text_emotion(self):
        ep = EmotionPerception()
        state = ep.perceive('voice.wav', 'face.png', text='I am very happy')
        self.assertEqual(state.overall(), 'happy')

    def test_model_mode(self):
        ep = EmotionPerception(use_model=True)
        state = ep.perceive('voice.wav', 'face.png')
        self.assertEqual(state.overall(), 'neutral')

if __name__ == '__main__':
    unittest.main()

import unittest
from ai_core import PersonalityEngine

class TestPersonalityEngine(unittest.TestCase):
    def test_update_and_style(self):
        engine = PersonalityEngine(momentum=0.5)
        # default vector should emphasize extraversion
        self.assertEqual(engine.vector[2], 1.0)
        engine.update('praise')
        self.assertNotEqual(engine.vector, [0.0] * 5)
        style = engine.get_personality_style()
        self.assertIsInstance(style, str)

if __name__ == '__main__':
    unittest.main()

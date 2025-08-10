import unittest
from ai_core import global_state

class TestGrowthStage(unittest.TestCase):
    def test_stage_progression(self):
        global_state.reset()
        # Initial stage should be enlighten by default
        self.assertEqual(global_state.get_growth_stage(), "enlighten")
        # Simulate some interactions and audio
        global_state.INTERACTION_COUNT = 25
        global_state.AUDIO_DATA_SECONDS = 400
        global_state.START_TIME -= global_state.datetime.timedelta(days=15)
        self.assertEqual(global_state.get_growth_stage(), "resonate")
        # Move to awaken stage
        global_state.INTERACTION_COUNT = 60
        global_state.AUDIO_DATA_SECONDS = 1000
        # Pretend 40 days passed
        global_state.START_TIME -= global_state.datetime.timedelta(days=40)
        self.assertEqual(global_state.get_growth_stage(), "awaken")

if __name__ == '__main__':
    unittest.main()

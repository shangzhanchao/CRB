import unittest
from ai_core import SemanticMemory

class TestSemanticMemory(unittest.TestCase):
    def test_add_and_query(self):
        memory = SemanticMemory(vector_dim=8, db_path="test.db")
        memory.add_memory("hi", "hello", "neutral", user_id="user1", touch_zone=2)
        results = memory.query_memory("hi", user_id="user1")
        self.assertTrue(len(results) > 0)
        self.assertEqual(results[0]["user_text"], "hi")
        self.assertEqual(results[0]["touch_zone"], 2)
        # verify SQLite persistence
        memory2 = SemanticMemory(vector_dim=8, db_path="test.db")
        self.assertGreaterEqual(len(memory2.records), 1)
        import os
        if os.path.exists("test.db"):
            os.remove("test.db")

if __name__ == '__main__':
    unittest.main()

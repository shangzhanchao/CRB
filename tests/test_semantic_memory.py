import unittest
from ai_core import SemanticMemory

class TestSemanticMemory(unittest.TestCase):
    def test_add_and_query(self):
        memory = SemanticMemory(vector_dim=8)
        memory.add_memory('hi', 'hello', 'neutral')
        results = memory.query_memory('hi')
        self.assertTrue(len(results) > 0)
        self.assertEqual(results[0]['user_text'], 'hi')

if __name__ == '__main__':
    unittest.main()

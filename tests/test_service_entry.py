import unittest
from service import handle_request

class TestServiceEntry(unittest.TestCase):
    def test_handle_request(self):
        data = {"robot_id": "robotA", "text": "hello"}
        resp = handle_request(data)
        self.assertTrue(all(resp[k] for k in ("text", "action", "expression", "audio")))
        self.assertIsInstance(resp["action"], list)

if __name__ == '__main__':
    unittest.main()

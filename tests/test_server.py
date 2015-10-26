"""
conversations/src/server/server.py tests
"""
import unittest
import twisted

class ConversationServerTestCase(unittest.TestCase):
    
    def setUp(self,):
        from conversations.src.server import server
        self.server = server

    def test_requestFactory(self):
        self.assertIsInstance(self.server.requestHandler.pages, dict)
        for each in self.server.requestHandler.pages:
            # assert that the dict values are all defined functions
            func = self.server.requestHandler.pages.get(each)
            self.assertIn('function', str(type(func)))

    def test_get_pages(self,):
        self.assertIsInstance(self.server.get_pages(), dict)




if __name__ == '__main__':
    unittest.main()

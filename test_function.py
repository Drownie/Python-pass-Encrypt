import unittest
from function import PasswordManager as pm

class PasswordManagerFunction(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.app = pm()
        self.app.connectDB()
    
    def test_createTable(self):
        out = self.app.createTable("create_user_table")
        self.assertDictEqual(out, {'success': True, 'message': "Table Successfully Created"})
    
    def test_login(self):
        out = self.app.login("test-02", "12345")
        self.assertDictEqual(out, {'success': True, 'message': 'Login Successful', 'data': [2, 'test-02', '6ZUcmSmCAiubOFmRXfYb2QE8gQnP37G0r-qyHnF4Rvw=']})

if __name__ == "__main__":
    unittest.main()
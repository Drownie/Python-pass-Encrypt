import unittest
from typer.testing import CliRunner

from pypass.pypass import PasswordManager as pm
from pypass import __app_name__, __version__, cli

runner = CliRunner()

class PasswordManagerFunction(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.app = pm()
        self.app.connectDB()
    
    def test_createTable(self):
        out = self.app.createTable("create_user_table")
        self.assertDictEqual(out, {'success': True, 'message': "Table Successfully Created"})
    
    def test_register(self):
        out = self.app.register("test-05", "12345", "12345", True)
        self.assertDictEqual(out, {'success': True, 'message': 'User Successfully Created'})
    
    def test_register_already_registered(self):
        out = self.app.register("test-01", "12345", "12345", True)
        self.assertDictEqual(out, {'success': False, 'message': 'User Already Registered'})

    def test_login(self):
        out = self.app.login("test-02", "12345")
        self.assertDictEqual(out, {'success': True, 'message': 'Login Successful', 'data': [2, 'test-02', '6ZUcmSmCAiubOFmRXfYb2QE8gQnP37G0r-qyHnF4Rvw=']})
    
    def test_login_wrong_password(self):
        out = self.app.login("test-02", "12344")
        self.assertDictEqual(out, {'success': False, 'message': 'Wrong Password', 'data': []})
    
    def test_login_unregistered_user(self):
        out = self.app.login("test-10", "12345")
        self.assertDictEqual(out, {'success': False, 'message': 'User Has Not Registered Yet', 'data': []})
    
    def test_insetData(self):
        out = self.app.insertData(1, "q0jfKDAB-Tkn0eMKswLp0Jya-atIWg63LxvOpOReYhM=", {'websiteAddress': "https://www.yahoo.com", 'username': "test122@gmail.com", 'password': "12344"}, True)
        self.assertDictEqual(out, {'success': True, 'message': "Insert Data Successfull"})
    
    def test_insertData_registered_account(self):
        out = self.app.insertData(1, "q0jfKDAB-Tkn0eMKswLp0Jya-atIWg63LxvOpOReYhM=", {'websiteAddress': "https://www.google.com", 'username': "test123@gmail.com", 'password': "12344"}, True)
        self.assertDictEqual(out, {'success': False, 'message': 'Account Already Registered'})

def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout

if __name__ == "__main__":
    unittest.main()
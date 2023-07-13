import json
from os.path import exists
import sqlite3
from sqlite3 import Error
from cryptography.fernet import Fernet
import bcrypt

class PasswordManager():
    def __init__(self) -> None:
        if not exists("sql.db"):
            open("sql.db", "w")

        self.commands = open("command.json", "r")
        self.commands = json.load(self.commands)

        self.salt = bcrypt.gensalt()

    def connectDB(self) -> None:
        conn = None
        try:
            conn = sqlite3.connect("sql.db")
        except Error as e:
            print("Error:", e)
        finally:
            if conn:
                self.conn = conn
        
    def createTable(self, commandName: str) -> dict:
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.commands[commandName])
        except Error as e:
            print("Error:", e)
            return {'success': False, 'message': e}
        finally:
            cursor.close()
            return {'success': True, 'message': "Table Successfully Created"}
    
    def register(self, username: str, password: str, confirmPassword: str, isTest: bool = False) -> dict:
        if password != confirmPassword:
            return {'success': False, 'message': "Password and Confirmation Password is not the same"}
        
        checkResult = self.checkRegisteredUser(username)
        if checkResult['success']:
            return {'success': False, 'message': checkResult['message']}
        
        hashedPassword = bcrypt.hashpw(password.encode("utf-8"), self.salt)
        key = Fernet.generate_key().decode("utf-8")

        try:
            cursor = self.conn.cursor()
            cursor.execute(self.commands["insert_user"], (username, hashedPassword, key))
        except Error as e:
            print("Error:", e)
            return {'success': False, 'message': e}
        finally:
            cursor.close()
            if not isTest: self.conn.commit()
            return {'success': True, 'message': "User Successfully Created"}
    
    def login(self, username: str, password: str) -> dict:
        checkResult = self.checkRegisteredUser(username)
        if not checkResult['success']:
            return {'success': False, 'message': checkResult['message'], 'data': []}
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.commands["find_user"], (username, ))
        except Error as e:
            return {'success': False, 'message': e, 'data': []}
        finally:
            userId, _, passwordHash, key = cursor.fetchone()
            cursor.close()

            if bcrypt.checkpw(password.encode("utf-8"), passwordHash):
                return {'success': True, 'message': "Login Successful", 'data': [userId, username, key]}
            return {'success': False, 'message': "Wrong Password", 'data': []}

    def checkRegisteredUser(self, username: str) -> dict:
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.commands["find_user"], (username, ))
        except Error as e:
            print("Error:", e)
            return {'success': False, 'message': e}
        finally:
            user = cursor.fetchone()
            cursor.close()
            if user is not None:
                return {'success': True, 'message': "User Already Registered"}
            return {'success': False, 'message': "User Has Not Registered Yet"}
    
    def viewUsers(self) -> tuple:
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.commands["select_users"])
        except Error as e:
            print("Error:", e)
            return {'success': False, 'message': e, 'data': []}
        finally:
            users = cursor.fetchall()
            for user in users:
                print(user)
            return {'success': True, 'message': '', 'data': users}

    def insertData(self, userId: int, key: str, data: dict, isTest: bool = False) -> dict:
        checkResult = self.checkRegisteredUserPM(data['websiteAddress'], data['username'])
        if checkResult['success']:
            return {'success': False, 'message': checkResult['message']}
        fernet = Fernet(key.encode("utf-8"))
        encryptedPassword = fernet.encrypt(data['password'].encode("utf-8"))
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.commands["insert_pm"], (userId, data['websiteAddress'], data['username'], encryptedPassword))
        except Error as e:
            print("Error:", e)
            return {'success': False, 'message': e}
        finally:
            cursor.close()
            if not isTest: self.conn.commit()
            return {'success': True, 'message': "Insert Data Successfull"}
    
    def checkRegisteredUserPM(self, websiteAddress: str, username: str) -> dict:
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.commands["find_user_pm"], (websiteAddress, username))
        except Error as e:
            print("Error:", e)
            return {'success': False, 'message': e}
        finally:
            account = cursor.fetchone()
            cursor.close()
            if account is not None:
                return {'success': True, 'message': "Account Already Registered"}
            return {'success': False, 'message': "Account Has Not Registered Yet"}

if __name__ == "__main__":
    test = PasswordManager()
    test.connectDB()
    test.createTable("create_user_table")
    test.createTable("create_pm_table")
    test.viewUsers()
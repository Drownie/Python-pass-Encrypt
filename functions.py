import json
from os.path import exists
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

class Functions:
    def __init__(self):
        if exists('data.json'):
            self.data = open("data.json", "r")
            self.users = json.load(self.data)['Users']
        else:
            tmplt = {"Users": {}}
            cnv = json.dumps(tmplt, indent=4)
            dataW = open("data.json", "w")
            dataW.write(cnv)
            self.users = {}
        
    def register(self, inp):
        # Check if the user is exist in the json file
        if self.users.get(inp[0]):
            return {"success": 0, "result": "User already exist"}

        # Generating Private Key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        
        # if not exist add the new user into the users variable
        pwd = bytes(inp[1], encoding="utf-8")
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(pwd)
        )
        
        # add new user to the self.users
        self.users[inp[0]] = {"PEM": pem.decode(encoding="utf-8"), "EncryptedData": []}
        tmpData = {"Users": self.users}
        cnv = json.dumps(tmpData, indent=4)
        
        # Write the new data into the json file
        dataW = open("data.json", "w")
        dataW.write(cnv)
        return {"success": 1, "result": "Registration Complete, please try login"}

    def authenticate(self, inp):
        # Check if the user exist
        user = self.users.get(inp[0])
        if user:
            pem = bytes(user['PEM'], encoding="utf-8")
            try:
                private_key = load_pem_private_key(pem, password=bytes(inp[1], encoding="utf-8"))
                return {"success": 1, "result": private_key, "user": inp[0]}
            except:
                return {"success": 0, "result": "Wrong Password"}
        else:
            # User not found
            return {"success": 0, "result": "User Not Found"}

    def addNewData(self, user, private_key, data):
        cnv = bytes(json.dumps(data), encoding="utf-8")
        public_key = private_key.public_key()
        cipher_text = public_key.encrypt(
            cnv,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        stringify = cipher_text.decode(encoding="ISO-8859-1")
        self.users[user]['EncryptedData'].append(stringify)
        tmpData = {"Users": self.users}
        cnv2 = json.dumps(tmpData, indent=4)
        
        # Write the new data into the json file
        dataW = open("data.json", "w")
        dataW.write(cnv2)
        return {"success": 1, "result": "Add successfully"}
    
    def decodeData(self, user, private_key, page, maksPerPage=5):
        tmpData = []
        encryptedData = self.users[user]['EncryptedData']
        maks_data = len(encryptedData)
        maks_per_page = maksPerPage
        lim = (page - 1) * maks_per_page
        if (page > 1 and maks_data > maks_per_page * (page - 1)):
            try:
                for i in range(min(maks_per_page, maks_data - ((page - 1) * maks_per_page))):
                    cipher_text = bytes(encryptedData[i + maks_per_page * (page -1)], encoding="ISO-8859-1")
                    plain_text = private_key.decrypt(
                        cipher_text,
                        padding.OAEP(
                            mgf=padding.MGF1(algorithm=hashes.SHA256()),
                            algorithm=hashes.SHA256(),
                            label=None
                        )
                    )
                    tmpData.append(json.loads(plain_text.decode("utf-8")))
            except:
                print("Error")
        else:
            for i in range(min(maks_data, maks_per_page)):
                try:
                    cipher_text = bytes(encryptedData[i], encoding="ISO-8859-1")
                    plain_text = private_key.decrypt(
                        cipher_text,
                        padding.OAEP(
                            mgf=padding.MGF1(algorithm=hashes.SHA256()),
                            algorithm=hashes.SHA256(),
                            label=None
                        )
                    )
                    tmpData.append(json.loads(plain_text.decode("utf-8")))
                except:
                    print("Error")
        return tmpData, maks_data

if __name__ == "__main__":
    functions = Functions()
    # print(functions.register(["Drownie15", "12345"]))
    res = functions.authenticate(["Drownie12", "12345"])
    print(res['result'])
    print(functions.decodeData("Drownie12", res['result'], 5, 1))
    # print(functions.addNewData("Drownie14", res['result'], {"site": "linux.com","username": "drownie20@linux.com","password": "12345"}))
    # print(functions.addNewData(res['result'], {"site": "www.google.com", "username": "drownie4@gmail.com", "password": "123444"}))
    # print(functions.addNewData(res['result'], {"site": "www.android.com", "username": "drownie1@gmail.com", "password": "123444"}))
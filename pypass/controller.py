from cryptography.fernet import Fernet
from typing import Any, Dict, NamedTuple
from pathlib import Path

from pypass import ERROR, SUCCESS
from pypass.database import DBHandler

class PyResponse(NamedTuple):
    status: int
    data: Dict[str, Any]

class PyPassManager:
    def __init__(self, db_path: Path, key: str):
        self._db_handler = DBHandler(db_path)
        self._db_handler.connect_db()
        self._db_handler.create_passdata_db()
        self._key = key
    
    def register_passdata(self, username: str, password: str, website_address: str) -> PyResponse:
        check_registered = self._db_handler.fetch_passdata({'website_address': website_address, 'username': username})
        if check_registered.status != SUCCESS: 
            return PyResponse(check_registered.status, {})
        
        fernet = Fernet(self._key.encode("utf-8"))
        hashed_password = fernet.encrypt(password.encode("utf-8"))

        data = {
            "username": username,
            "password": hashed_password,
            "website_address": website_address
        }

        result = self._db_handler.insert_passdata(data)
        return PyResponse(result.status, result.data)

    def update_passdata(self, pass_id: str, username: str, password: str, website_address: str) -> PyResponse:
        check_registered = self._db_handler.fetch_passdata_by_id(pass_id)
        if check_registered.status != SUCCESS:
            return PyResponse(ERROR, [])
        
        fernet = Fernet(self._key.encode("utf-8"))
        hashed_password = fernet.encrypt(password.encode("utf-8"))

        data = {
            "username": username,
            "password": hashed_password,
            "website_address": website_address,
            "pass_id": pass_id
        }

        result = self._db_handler.update_passdata(data)
        return PyResponse(result.status, result.data)

    def get_passdata(self, pass_id: int) -> PyResponse:
        result = self._db_handler.fetch_passdata_by_id(pass_id)
        return PyResponse(result.status, result.data)

    def get_all_passdata(self, page: int, decrypt: bool = False) -> PyResponse:
        result = self._db_handler.fetch_passdata_all(page)
        fernet = Fernet(self._key.encode('utf-8'))
        if not decrypt:
            return PyResponse(result.status, result.data)

        decodedData = []
        for i, passData in enumerate(result.data):
            tmp = [data for data in result.data[i]]
            tmp[-1] = fernet.decrypt(passData[-1]).decode('utf-8')
            decodedData.append(tmp)
        return PyResponse(result.status, decodedData)
    
    def search_passdata(self, username: str, website_address: str, page: int, decrypt: bool = False) -> PyResponse:
        data = {
            "username": "%" + username + "%",
            "websiteAddress": "%" + website_address + "%",
            "page": page
        }
        result = self._db_handler.find_passdata(data)
        fernet = Fernet(self._key.encode('utf-8'))
        if not decrypt:
            return PyResponse(result.status, result.data)

        decodedData = []
        for i, passData in enumerate(result.data):
            tmp = [data for data in result.data[i]]
            tmp[-1] = fernet.decrypt(passData[-1]).decode('utf-8')
            decodedData.append(tmp)
        return PyResponse(result.status, decodedData)

    def delete_passdata(self, pass_id: int) -> PyResponse:
        check_registered = self._db_handler.fetch_passdata_by_id(pass_id)
        if check_registered.status != SUCCESS:
            return PyResponse(ERROR, [])
        
        result = self._db_handler.delete_passdata(pass_id)

        return PyResponse(result.status, result.data)
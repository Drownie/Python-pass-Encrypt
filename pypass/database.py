import configparser
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, NamedTuple
from sqlite3 import Error

from pypass import DB_WRITE_ERROR, SUCCESS, SQL_ERROR, DB_READ_ERROR, CONFLICT_ERROR, ERROR

DEFAULT_DB_FILE_PATH = Path.home().joinpath("." + Path.home().stem + "_sql.db")

def get_database_path(config_file: Path) -> Path:
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])

def get_key(config_file: Path) -> str:
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return config_parser["General"]["key"]

def init_database(db_path: Path) -> int:
    try:
        db_path.write_text("")
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR

class DBResponse(NamedTuple):
    status: int
    data: List[Dict[str, Any]]

class DBHandler:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def connect_db(self) -> DBResponse:
        self.connection = None
        try:
            self.connection = sqlite3.connect(self._db_path)
            return DBResponse(SUCCESS, [])
        except Error:
            return DBResponse(SQL_ERROR, [])

    def create_passdata_db(self) -> DBResponse:
        command = "CREATE TABLE IF NOT EXISTS passdata(id INTEGER PRIMARY KEY,\n websiteAddress CHAR(100),\n username CHAR(50) NOT NULL,\n password CHAR(20) NOT NULL);"
        try:
            cursor = self.connection.cursor()
            cursor.execute(command)
            self.connection.commit()
            cursor.close()
            return DBResponse(SUCCESS, [])
        except Error:
            return DBResponse(SQL_ERROR, [])
    
    def insert_passdata(self, data: dict) -> DBResponse:
        command = "INSERT INTO passdata(websiteAddress, username, password) VALUES (?, ?, ?);"
        try:            
            cursor = self.connection.cursor()
            cursor.execute(command, (data['website_address'], data['username'], data['password']))
            self.connection.commit()
            cursor.close()
            return DBResponse(SUCCESS, [])
        except Error:
            return DBResponse(DB_WRITE_ERROR, [])
    
    def fetch_passdata_all(self) -> DBResponse:
        command = "SELECT id, websiteAddress, username, password FROM passdata;"
        try:
            cursor = self.connection.cursor()
            cursor.execute(command)
            passdata = cursor.fetchmany(10)
            cursor.close()
            return DBResponse(SUCCESS, passdata)
        except Error:
            return DBResponse(DB_READ_ERROR, [])     

    def fetch_passdata(self, data: dict) -> DBResponse:
        command = "SELECT id, websiteAddress, username FROM passdata WHERE websiteAddress = ? AND username = ?;"
        try:
            cursor = self.connection.cursor()
            cursor.execute(command, (data['website_address'], data['username'], ))
            passdata = cursor.fetchone()
            cursor.close()
            if passdata is None:
                return DBResponse(SUCCESS, [])
            return DBResponse(CONFLICT_ERROR, passdata)
        except Error:
            return DBResponse(DB_READ_ERROR, [])
    
    def fetch_passdata_by_id(self, pass_id: str) -> DBResponse:
        command = "SELECT id, websiteAddress, username FROM passdata WHERE id = ?;"
        try:
            cursor = self.connection.cursor()
            cursor.execute(command, (pass_id, ))
            passdata = cursor.fetchone()
            cursor.close()
            if passdata is None:
                return DBResponse(ERROR, [])
            return DBResponse(SUCCESS, passdata)
        except Error:
            return DBResponse(DB_READ_ERROR, [])

    def update_passdata(self, data: dict) -> DBResponse:
        command = "UPDATE passdata SET websiteAddress = ?, username = ?, password = ? WHERE id = ?;"
        try:
            cursor = self.connection.cursor()
            cursor.execute(command, (data['website_address'], data['username'], data['password'], data['pass_id'], ))
            self.connection.commit()
            cursor.close()
            return DBResponse(SUCCESS, [])
        except Error:
            return DBResponse(DB_WRITE_ERROR, [])
    
    def delete_passdata(self, pass_id: str) -> DBResponse:
        command = "DELETE FROM passdata WHERE id = ?;"
        try:
            cursor = self.connection.cursor()
            cursor.execute(command, (pass_id, ))
            self.connection.commit()
            cursor.close()
            return DBResponse(SUCCESS, [])
        except Error:
            return DBResponse(DB_WRITE_ERROR, [])
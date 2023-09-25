import pytest
from typer.testing import CliRunner
from cryptography.fernet import Fernet

from pypass import (
    __app_name__, 
    __version__, 
    cli,
    controller,
    SUCCESS,
    DB_READ_ERROR,
    DB_WRITE_ERROR
)

runner = CliRunner()

def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout

@pytest.fixture
def mock_db_file(tmp_path):
    db_file = tmp_path / "sql.db"
    return db_file

test_data_1 = {
    "username": "drownie",
    "password": "12345",
    "website": "google.com",
    "expected": SUCCESS
}

test_data_2 = {
    "username": "drownie2",
    "password": "12345",
    "website": "yahoo.com",
    "expected": SUCCESS
}

@pytest.mark.parametrize(
    "username, password, website, expected",
    [
        pytest.param(
            test_data_1["username"],
            test_data_1["password"],
            test_data_1["website"],
            test_data_1["expected"]
        ),
        pytest.param(
            test_data_2["username"],
            test_data_2["password"],
            test_data_2["website"],
            test_data_2["expected"]
        ),
    ],
)
def test_add(mock_db_file, username, password, website, expected):
    pypass = controller.PyPassManager(mock_db_file, Fernet.generate_key().decode('utf-8'))
    assert pypass.register_passdata(username, password, website).status == expected
    read = pypass.get_all_passdata()
    assert len(read.data) == 1

"""This module provides the Daka database functionality."""

import configparser
from pathlib import Path
from typing import Dict, Union, List, NamedTuple
import json

from daka import DB_WRITE_ERROR, SUCCESS

DEFAULT_DB_DIR_PATH = Path.home().joinpath('.config/daka')
DEFAULT_DB_FILE_PATH = DEFAULT_DB_DIR_PATH / "db.json"

def get_database_path(config_file: Path) -> Path:
    """Return the current path to the Daka database."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])

# TODO def set_database_path

def init_database(db_path: Path) -> int:
    """Create the Daka database."""
    try:
        db_path.write_text("[]")  # Empty to-do list
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR
    
class DBResponse(NamedTuple):
    timer_list: List[Dict[str, Union[str, int]]]
    error: int

class DatabaseHandler:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def read_timers(self) -> DBResponse:
        try:
            with self._db_path.open("r") as db:
                try:
                    return DBResponse(json.load(db), SUCCESS)
                except json.JSONDecodeError:  # Catch wrong JSON format
                    return DBResponse([], JSON_ERROR)
        except OSError:  # Catch file IO problems
            return DBResponse([], DB_READ_ERROR)

    def write_timers(self, timer_list: List[Dict[str, Union[str, int]]]) -> DBResponse:
        try:
            with self._db_path.open("w") as db:
                json.dump(timer_list, db, indent=4)
            return DBResponse(timer_list, SUCCESS)
        except OSError:  # Catch file IO problems
            return DBResponse(timer_list, DB_WRITE_ERROR)
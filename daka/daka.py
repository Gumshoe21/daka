"""This module provides the Daka model-controller."""

from pathlib import Path
from typing import Any, Dict, List, NamedTuple, Union
from daka import DB_READ_ERROR, ID_ERROR
from daka.database import DatabaseHandler, DBResponse

class CurrentTimer(NamedTuple):
    metadata: Dict[str, Union[str, int]]
    error: int

class Timer:
	def __init__(self, name: str, mode: str, duration: int) -> None:
		self.name = name
		self.mode = mode
		self.duration = duration

class Daka:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)
    # TODO enforce unique timer name
    def add(self, mode: str, name: str, duration: int) -> CurrentTimer:
        metadata = {
            "name": name,
			"mode": mode,
			"duration": duration,
   		}
        read_db: DBResponse = self._db_handler.read_timers()
        if read_db.error == DB_READ_ERROR:
            return CurrentTimer(metadata, read_db.error) 
        read_db.timer_list.append(metadata)
        write_db = self._db_handler.write_timers(read_db.timer_list)
        return CurrentTimer(metadata, write_db.error)
    
    def list(self) -> List[Dict[str, Any]]:
        read_db = self._db_handler.read_timers()
        return read_db.timer_list

	# TODO add remove fn
	# TODO add edit fn
	# TODO add purge (delete all) fn
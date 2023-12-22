"""This module provides the Daka model-controller."""

from pathlib import Path
from typing import Any, Dict, List, NamedTuple
from rptodo import DB_READ_ERROR, ID_ERROR
from rptodo.database import DatabaseHandler

class CurrentTodo(NamedTuple):
    todo: Dict[str, Any]
    error: int

class Timer:
	def __init__(self, name: str, mode: str, duration: int) -> None:
		self.name = name
		self.mode = mode
		self.duration = duration

		

class Daka:
    def __init__(self, db_path: Path) -> None:
        self.db_handler = DatabaseHandler(db_path)
    # TODO enforce unique timer name
    def add(self, name: str, mode: str, duration: str):
     	timer = Timer(name, mode, duration)
     	metadata = {
      		"name": name,
			"mode": mode,
			"duration": duration
		}
     	read_db = self._db_handler.read_timers()
      	if read_db.error == DB_READ_ERROR:
			return timer
		read_db.timer_list.append(metadata)
		write_db = self._db_handler.write_timers(read_db.timer_list)
		return timer

	def list(self) -> List[Dict[str, Any]]:
		read_db = self._db_handler.read_timers()
		return read_db.timer_list

	def remove(self, timer_id)

class Todoer:
    def set_done(self, todo_id: int) -> CurrentTodo:
        """Set a to-do as done."""
        read = self._db_handler.read_todos()
        if read.error:
            return CurrentTodo({}, read.error)
        try:
            todo = read.todo_list[todo_id - 1]
        except IndexError:
            return CurrentTodo({}, ID_ERROR)
        todo["Done"] = True
        write = self._db_handler.write_todos(read.todo_list)
        return CurrentTodo(todo, write.error)
    
    def remove(self, todo_id: int) -> CurrentTodo:
        """Remove a to-do from the database using its id or index."""
        read = self._db_handler.read_todos()
        if read.error:
            return CurrentTodo({}, read.error)
        try:
            todo = read.todo_list.pop(todo_id - 1)
        except IndexError:
            return CurrentTodo({}, ID_ERROR)
        write = self._db_handler.write_todos(read.todo_list)
        return CurrentTodo(todo, write.error)
    
    def remove_all(self) -> CurrentTodo:
        """Remove all to-dos from the database."""
        write = self._db_handler.write_todos([])
        return CurrentTodo({}, write.error)
"""Top-level package for Daka."""

# defne two module-level names to hold app's name and version
# https://www.python.org/dev/peps/pep-0008/#module-level-dunder-names
__app_name__ = "daka"
__version__ = "0.1.0"

# define series of return and error codes and assign integer numbers to each using range
# https://en.wikipedia.org/wiki/Error_code
(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    DB_READ_ERROR,
    DB_WRITE_ERROR,
    JSON_ERROR,
    ID_ERROR,
) = range(7)

# ERRORS is a dictionary that maps error codes to human-readable error messages. You’ll use these messages to tell the user what’s happening with the application.

ERRORS = {
    DIR_ERROR: "config directory error",
    FILE_ERROR: "config file error",
    DB_READ_ERROR: "database read error",
    DB_WRITE_ERROR: "database write error",
    ID_ERROR: "daka id error",
}
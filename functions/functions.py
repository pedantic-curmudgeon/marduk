"""Custom string and database functions."""

import time
from sqlalchemy.engine.base import Engine
from sqlalchemy.exc import OperationalError

# Define string functions.

def stringify_list(list_: list,
                   quoted: bool = False
                   ) -> str:
    """Converts a list to a string representation.

    Accepts a list of mixed data type objects and returns a string
    representation. Optionally encloses each item in single-quotes.

    Args:
        list_: The list to convert to a string.
        quoted: Indicates if the items in the list should be in quotes.

    Returns:
        A string representation of the list.
    """
    if quoted:
        string_ = ', '.join(f"'{i}'" for i in list_)
    else:
        string_ = ', '.join(f'{i}' for i in list_)

    return string_


# Define database functions.

def db_alive(engine: Engine,
             wait_max: int = 60,
             wait_increment: int = 5
             ) -> bool:
    """Checks if a database is alive and accepting queries.

    Executes a query using the SQL Alchemy engine at intervals
    defined by the wait increment up until the wait max.

    Args:
        engine: SQL Alchemy database engine.
        wait_max: Maximum wait time in seconds.
        wait_increment: Time between query attempts in seconds.

    Returns:
        A boolean indicating if the database is alive.
    """
    # Define core variables.
    sql = 'select * from information_schema.schemata;'
    wait_time = 0
    db_alive = False

    # Check for database response.
    while not db_alive and wait_time < wait_max:
        if wait_time <= wait_max:
            try:
                engine.execute(sql)
                db_alive = True
            except OperationalError:
                time.sleep(wait_increment)
                wait_time += wait_increment

    return db_alive

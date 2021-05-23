"""Custom functions."""

import time
from sqlalchemy.engine.base import Engine
from sqlalchemy.exc import OperationalError


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


def db_alive(engine: Engine,
             wait_max: int = 60,
             wait_increment: int = 5
             ) -> bool:
    """Checks if a database is alive and accepting queries.

    Executes a query using the SQL Alchemy engine at intervals
    defined by the wait increment up until the wait max.

    Args:
        wait_max: Maximum wait time in seconds.
        wait_increment: Time between query attempts in seconds.

    Returns:
        A boolean indicating if the database is alive.
    """
    # Define core variables.
    sql = 'select * from information_schema.schemata;'
    wait_time = 0
    db_alive = False
    results = None

    # Check for database response.
    while not db_alive:
        if wait_time <= wait_max:
            print(wait_time)
            try:
                results = engine.execute(sql)
                db_alive = True
            except OperationalError:
                time.sleep(wait_increment)
                wait_time += wait_increment

    print('results:', results.fetchall())
    print('db_alive:', db_alive)
    return db_alive

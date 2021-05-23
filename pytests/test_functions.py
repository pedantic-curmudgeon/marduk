"""Defines a test class with scenarios for the functions module."""

import datetime as dt
from marduk.database.engines import compose_db
from marduk import functions


class TestFunctions():
    """Test class containing scenarios for the functions module."""

    # Define __init__-like parameters.
    db_engine = compose_db


    # Define string tests.

    def test_stringify_list_001(self) -> None:
        """Tests stringify_list without quoted output."""
        # Define input list.
        input_list = [1, 2, 'a', 'b']

        # Define expected string output.
        exp = '1, 2, a, b'

        # Get actual string output.
        got = functions.stringify_list(list_=input_list, quoted=False)

        # Test output.
        assert got == exp


    def test_stringify_list_002(self) -> None:
        """Tests stringify_list with quoted output."""
        # Define input list.
        input_list = [1, 2, 'a', 'b']

        # Define expected string output.
        exp = "'1', '2', 'a', 'b'"

        # Get actual string output.
        got = functions.stringify_list(list_=input_list, quoted=True)

        # Test output.
        assert got == exp


    # Define database tests.

    def test_query_db_001(self) -> None:
        """Tests querying the Liquibase-updated database."""
        # Define expected output.
        exp = [(75, 'Seventy-five', dt.datetime(1975, 7, 5, 0, 0))]

        # Define SQL query.
        sql = 'select * from main.liquid;'

        # Get actual output.
        got = self.db_engine.execute(sql)
        got = got.fetchall()

        # Test output.
        assert got == exp

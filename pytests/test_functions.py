"""Defines a test class with scenarios for the functions module."""

import datetime as dt
from marduk.database.engines import compose_db
from marduk import functions
import os
from sqlalchemy import create_engine


class TestFunctions():
    """Test class containing scenarios for the functions module."""

    # Define setup method.

    def setup_class(self) -> None:
        """Sets up the test class."""
        self.db_engine = compose_db
        if not functions.db_alive(self.db_engine):
            msg = 'Unable to connect to test database.'
            raise ConnectionError(msg)


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

    def test_db_alive_001(self) -> None:
        """Tests db_alive with a non-existent database."""
        # Define non-existent database engine inputs.
        db_cfg = {
            'user': 'bad_user',
            'password': 'bad_password',
            'server': 'bad_server',
            'port': 3306,
            'db': 'bad_db',
            'charset': 'utf8mb4'
        }

        db_engine = create_engine(
            ("mysql+pymysql://{user}:{password}@{server}:{port}/{db}"
            "?charset={charset}").format(**db_cfg),
            pool_recycle=3600
        )

        # Get results.
        result = functions.db_alive(
            engine=db_engine,
            wait_max=2,
            wait_increment=1
        )

        # Test results.
        assert not result


    def test_db_alive_002(self) -> None:
        """Tests db_alive with an active database."""
        # Get results.
        result = functions.db_alive(
            engine=self.db_engine,
            wait_max=3,
            wait_increment=1
        )

        # Test results.
        assert result


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


    # Define environment variable tests.

    def test_environment_variable_001(self) -> None:
        """Tests the ENV_VAR environment variable value."""
        # Define expected output.
        exp = 'abc123def456'

        # Get actual output.
        got = os.environ['ENV_VAR']

        # Test output.
        assert got == exp

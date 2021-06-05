import click
import pytest
from marduk.database import compose_db
from marduk.functions import db_alive


@click.command()
def run_tests():
    """Executes all tests in the folder."""
    if db_alive(compose_db):
        pytest.main(['-v', '--junitxml=auto_tests.xml'])
    else:
        msg = 'Unable to connect to test database.'
        raise ConnectionError(msg)

if __name__ == '__main__':
    run_tests()

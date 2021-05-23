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


# NOTE:
# VS Code Interpreter: ~/.pyenv/versions/3.8.2/bin/python3
# cd to ~/.pyenv/versions/3.8.2/lib/python3.8/site-packages/marduk/pytests
# pyenv shell 3.8.2
# Run Command: python runner.py >auto_tests.txt

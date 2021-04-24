import click
import pytest


@click.command()
def run_tests():
    """Executes all tests in the folder."""
    pytest.main(['-v', '--junitxml=auto_tests.xml'])

if __name__ == '__main__':
    run_tests()


# NOTE:
# VS Code Interpreter: ~/.pyenv/versions/3.8.2/bin/python3
# cd to ~/.pyenv/versions/3.8.2/lib/python3.8/site-packages/marduk/pytests
# pyenv shell 3.8.2
# Run Command: python runner.py

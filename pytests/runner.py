import click
from pathlib import Path
import pytest

root_folder = Path(__file__).parents[1]
folder_name = root_folder.name


@click.command()
def run_tests():
    """Executes all tests in the folder."""
    pytest.main([
        '-v',
        '--junitxml=auto_tests.xml',
        f'--cov={folder_name}',
        '--cov-branch',
        '--cov-report=xml',
        '--cov-report=html',
        '--cov-report=term'
        ]
    )


if __name__ == '__main__':
    run_tests()

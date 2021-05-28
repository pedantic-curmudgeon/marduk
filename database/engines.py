"""Standard database engines."""

from dotenv import dotenv_values
from pathlib import Path
from sqlalchemy import create_engine


# Get database environment variables.
this_folder = Path(__file__).parent
root_folder = this_folder.parent
env_file = root_folder / 'docker' / '.env.test.local'
env_dict = dotenv_values(env_file)
db_name = env_dict['DB_NAME']
db_user = env_dict['DB_USER']
db_password = env_dict['DB_PASSWORD']

# Define database engine for Docker Compose connectivity.
compose_db_cfg = {
    'user': db_user,
    'password': db_password,
    'server': 'db_container', # This corresponds to the name of the DB container in the compose file.
    'port': '3306',
    'db': db_name,
    'charset': 'utf8mb4'
}

compose_db = create_engine(
    ("mysql+pymysql://{user}:{password}@{server}:{port}/{db}"
     "?charset={charset}").format(**compose_db_cfg),
     pool_recycle=3600
)

# Define database engine for local Docker Container connectivity.
container_db_cfg = {
    'user': db_user,
    'password': db_password,
    'server': 'localhost',
    'port': '3306',
    'db': db_name,
    'charset': 'utf8mb4'
}

container_db = create_engine(
    ("mysql+pymysql://{user}:{password}@{server}:{port}/{db}"
     "?charset={charset}").format(**container_db_cfg),
     pool_recycle=3600
)

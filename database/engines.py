"""Standard database engines."""

from sqlalchemy import create_engine


# Define database engine for Docker Compose connectivity.
compose_db_cfg = {
    'user': 'root',
    'password': 'my-secret-pw',
    'server': 'db_container', # This corresponds to the name of the DB container in the compose file.
    'port': '3306',
    'db': 'main',
    'charset': 'utf8mb4'
}

compose_db = create_engine(
    ("mysql+pymysql://{user}:{password}@{server}:{port}/{db}"
     "?charset={charset}").format(**compose_db_cfg),
     pool_recycle=3600
)

# Define database engine for local Docker Container connectivity.
container_db_cfg = {
    'user': 'root',
    'password': 'my-secret-pw',
    'server': 'localhost',
    'port': '3306',
    'db': 'main',
    'charset': 'utf8mb4'
}

container_db = create_engine(
    ("mysql+pymysql://{user}:{password}@{server}:{port}/{db}"
     "?charset={charset}").format(**container_db_cfg),
     pool_recycle=3600
)

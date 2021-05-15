import pandas as pd
import sqlalchemy


# Define MariaDB connection details.

# https://docs.sqlalchemy.org/en/14/dialects/mysql.html

db_cfg = {
    'user': 'root',
    'password': 'my-secret-pw',
    'server': 'localhost',
    'port': '3306',
    'db': 'main',
    'charset': 'utf8mb4'
}

# NOTE: Paren-wrapped string literals don't use commas to cross lines!
# NOTE: Can use "mariadb+pymysql" if MariaDB connector is installed.
engine = sqlalchemy.create_engine(
    ("mysql+pymysql://{user}:{password}@{server}:{port}/{db}"
     "?charset={charset}").format(**db_cfg),
     pool_recycle=3600
)

# engine = sqlalchemy.create_engine(
#     "mysql+pymysql://{user}:{password}@{server}/{db}?charset=utf8mb4".format(**db_cfg),
#     pool_recycle=3600
# )

sql = 'select * from my_table;'

df = pd.read_sql(sql=sql, con=engine)

print(df)
print(df.dtypes)

data = {
    'col1': [1, 2, 3],
    'col2': ['a', 'b', 'c'],
    'col3': ['1990-07-07', '2000-07-07', '2010-07-07']
}

df = pd.DataFrame(data)
df['col3'] = pd.to_datetime(df['col3'])

df.to_sql(name='my_table', con=engine, if_exists='append', index=False)

sql_write = '''insert into my_table values (4, 'd', '2020-07-07');'''
sql_read = '''select * from my_table;'''

# NOTE: Autocommit should only be used for writing transactions, NOT reading.
# https://docs.sqlalchemy.org/en/14/core/connections.html#understanding-autocommit

# NOTE: Autocommit shouldn't need to be set per the above! Leaving info on how to set in case actually needed.
# conn = engine.connect().execution_options(autocommit=True)

with engine.connect() as conn:
    conn.execute(sql_write)

results = engine.execute(sql_read)
results_all = results.fetchall()
keys = results.keys()

print(results_all)
print(keys)

sql = '''select * from my_table where col3 > '2000-07-07';'''
df = pd.read_sql(sql=sql, con=engine)
print(df)
print(df.dtypes)

# Running Docker container:
# https://hub.docker.com/_/mariadb
# NOTE: Refer to `Where to Store Data` section for where to store the data.

# ```docker pull mariadb:10.5.9```
# ```docker run -p 127.0.0.1:3306:3306  --name some-mariadb -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mariadb:tag```
#  ```docker run -p 127.0.0.1:3306:3306  --name some-mariadb -e MYSQL_ROOT_PASSWORD=my-secret-pw -e MYSQL_DATABASE=main -d mariadb:10.5.9```

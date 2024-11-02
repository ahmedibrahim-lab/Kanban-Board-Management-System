import sys
from sqlalchemy import create_engine, text
import config

db_param = config.Config()
user = db_param.MYSQL_USER
password = db_param.MYSQL_PASSWORD
host = db_param.MYSQL_HOST
port = db_param.MYSQL_PORT
db = db_param.MYSQL_DB


# function can work with 2 option value: DROP - will only drop database, DELETE - if database exists, it will be dropped
# and initialized again. By default, (empty option) existing database won't be dropped, but will create if not exists.
# Running from terminal:
# ...\Kanban-Board-Management-System> python .\db_init.py
# ...\Kanban-Board-Management-System> python .\db_init.py DELETE
# ...\Kanban-Board-Management-System> python .\db_init.py DROP
def db_create(with_sample_datas):
    db_engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}")
    with db_engine.connect() as con:
        con.execute(text(f"CREATE DATABASE IF NOT EXISTS {db}"))

    db_engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}")   # USE db;

    with db_engine.connect() as con:
        with open(f"./mysql/{db}_ddl.sql") as file:
            sql_commands = file.read().split(';')  # Split by semicolons
            for command in sql_commands:
                if command.strip():  # Skip any empty statements
                    con.execute(text(command.strip()))

        with open(f"./mysql/{db}_triggers.sql") as file:
            sql_commands = file.read().split('//')
            for command in sql_commands:
                if command.strip() and command.strip().lower() != 'delimiter':   # not empty and not 'delimiter' only
                    con.execute(text(command.strip()))

        if with_sample_datas == 'y':
            with open(f"./mysql/{db}_sample_datas.sql") as file:
                sql_commands = file.read().split(';')  # Split by semicolons
                for command in sql_commands:
                    if command.strip():  # Skip any empty statement
                        con.execute(text(command.strip()))


def db_initialization(option):

    try:
        db_engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}")
        if option == 'DELETE':
            with db_engine.connect() as con:
                con.execute(text(f"DROP DATABASE {db};"))
                print(f"{db} database deleted, initializing again with sample datas? (y/n).")

            with_sample_datas = input("'y'/'n': ")
            db_create(with_sample_datas)

        elif option == 'DROP':
            with db_engine.connect() as con:
                con.execute(text(f"DROP DATABASE {db};"))
                print(f"{db} database dropped, exiting program.")
                exit()
        else:
            with db_engine.connect():
                pass
            print(f"{db} already exists. To delete and initialize again run with 'DELETE' argument.\n"
                  f"To drop {db} database without initializing a new one, use 'DROP' argument."
                  f"\nExiting program.")
            exit()

    except (Exception,):
        if option in ('DROP', 'DELETE'):
            print(f"No {db} database found, exiting.")
            exit()

        print(f"{db} database does not exists, initializing with sample datas? (y/n).")
        with_sample_datas = input("'y'/'n': ")
        db_create(with_sample_datas)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_option = sys.argv[1]
    else:
        user_option = None

    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}")

    try:
        with engine.connect() as connection:
            print("connected to MYSQL")

        db_initialization(user_option)
    except Exception as err:
        print("Config file error:\n", err)
        exit()

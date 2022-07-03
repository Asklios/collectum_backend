import sys
import time

from pg8000.dbapi import Connection, DatabaseError, Cursor
from pg8000.exceptions import InterfaceError

from backend import settings
from backend.database.pg_init_v1 import v1_tables
from backend.public_endpoints import health

DB_VERSION = 1

params = {'host': settings.POSTGRES_URL,
          'port': settings.POSTGRES_PORT,
          'user': settings.POSTGRES_USER,
          'password': settings.POSTGRES_PASSWORD
          }


def _ensuring_conn():
    try:
        return Connection(**params)
    except InterfaceError as e:
        print("[DB]: " + str(e.args[0]))
        return None
    except DatabaseError as e:
        print("[DB]: " + str(e.args[0]['M']))
        return None


def _get_conn() -> Connection:
    conn = _ensuring_conn()
    recon = False
    if conn is None:
        print("[DB]: No Connection. Trying to reconnect in some Seconds.")
        health.health['db'] = False
        recon = True
        time.sleep(30)
        init_db()
    if recon:
        health.health['db'] = True
    return conn


def get_conn(func):
    def try_conn(*args):
        conn = _ensuring_conn()
        if conn is None:
            health.health['db'] = False
            sys.exit()
        health['db'] = True
        cur = conn.cursor()
        return func(conn=conn, cur=cur, *args)
    return try_conn


def init_db() -> int:
    """
    Initiates the postgres database by creating the required tables and updating the db_version if required.
    """
    conn: Connection = _get_conn()
    cur: Cursor = conn.cursor()
    cur.execute('SELECT version()')
    print("[DB]: Connected to database")
    print("[DB]: " + cur.fetchone()[0])
    print("[DB]: Creating missing tables...")
    cur.execute('CREATE TABLE IF NOT EXISTS db_version('
                'id SERIAL PRIMARY KEY,'
                'version INTEGER UNIQUE)')
    conn.commit()
    cur.execute('SELECT MAX(version) FROM db_version')
    db_version: int = cur.fetchone()[0]
    if db_version is None:
        db_version = DB_VERSION
        cur.execute('INSERT INTO db_version(version) VALUES(%s)', (db_version,))
        conn.commit()
    elif db_version == 1:
        v1_tables(conn)
    else:
        print("[ERROR]: there is no matching db version")

    print("[DB]: current db version: " + str(db_version))

    conn.close()
    return db_version

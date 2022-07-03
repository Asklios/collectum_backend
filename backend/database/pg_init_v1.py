from pg8000.dbapi import Connection, Cursor

from backend import settings


def v1_tables(conn: Connection):
    cur: Cursor = conn.cursor()
    cur.execute(f"SET timezone = '{settings.PG_TIMEZONE}'")

    cur.execute('CREATE TABLE IF NOT EXISTS projects('
                'id SERIAL PRIMARY KEY,'
                'name VARCHAR(255) NOT NULL,'
                'description TEXT,'
                'version Integer NOT NULL,'
                'specification JSON NOT NULL,'
                'UNIQUE (name, version))')
    conn.commit()
    cur.execute('CREATE TABLE IF NOT EXISTS data('
                'id SERIAL PRIMARY KEY,'
                'timestamp TIMESTAMP,'
                'user_id TEXT NOT NULL,'
                'user_name TEXT NOT NULL,'
                'project_id INTEGER NOT NULL,'
                'project_version INTEGER NOT NULL,'
                'data_id INTEGER NOT NULL,'
                'data_version INTEGER NOT NULL,'
                'data JSON NOT NULL,'
                'UNIQUE (project_id, data_id, data_version),'
                'CONSTRAINT fk_project FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE)')
    conn.commit()

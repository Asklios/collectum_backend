import json
from typing import List

from pg8000.dbapi import Connection, DatabaseError, Cursor

from backend.database import pg_helper
from backend.database.dtos import Data, Project
from backend.database.pg_helper import get_conn


def init_db():
    pg_helper.init_db()


@get_conn
def add_data(data: Data, conn: Connection = None, cur: Cursor = None) -> Data | str:
    """
    Adds a new data to the database.
    """
    db_data = (data.timestamp, data.user_id, data.user_name, data.project_id, data.project_version, data.data_id,
               data.data_version, data.data)
    try:
        cur.execute("INSERT INTO data (timestamp, user_id, user_name, project_id, project_version, data_id, "
                    "data_version, data) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id", db_data)
        data.id = cur.fetchone()[0]
    except DatabaseError as e:
        conn.rollback()
        conn.close()
        return e.args[0]['M']
    conn.commit()
    conn.close()
    return data


@get_conn
def get_latest_data(project_id: int, conn: Connection = None, cur: Cursor = None) -> List[Data] | None | str:
    """
    Returns the latest data for a project.
    """
    try:
        cur.execute("SELECT DISTINCT ON (data_id) id, timestamp, user_id, user_name, project_id, project_version, "
                    "data_id, data_version, data FROM data WHERE project_id = %s ORDER BY data_id, data_version DESC",
                    (project_id,))
        data = cur.fetchall()
    except DatabaseError as e:
        conn.rollback()
        conn.close()
        return e.args[0]['M']
    conn.close()
    if data is None:
        return None
    return [Data(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]) for data in data]


@get_conn
def get_data_history(project: int, data_id: int, conn: Connection = None, cur: Cursor = None)\
        -> List[Data] | None | str:
    """
    Returns the data history.
    """
    try:
        cur.execute("SELECT id, timestamp, user_id, user_name, project_id, project_version, data_id, data_version, "
                    "data FROM data WHERE project_id = %s AND data_id = %s ORDER BY data_version DESC",
                    (project, data_id))
        data = cur.fetchall()
    except DatabaseError as e:
        conn.rollback()
        conn.close()
        return e.args[0]['M']
    conn.close()
    if data is None:
        return None
    return [Data(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]) for data in data]


@get_conn
def add_project(project: Project, conn: Connection = None, cur: Cursor = None) -> Project | str:
    """
    Adds a new project to the database.
    """
    db_project = (project.name, project.description, project.version, json.dumps(project.specification))
    try:
        cur.execute(
            "INSERT INTO projects (name, description, version, specification) VALUES (%s,%s,%s,%s) RETURNING id",
            db_project)
        project.id = cur.fetchone()[0]
    except DatabaseError as e:
        conn.rollback()
        conn.close()
        return e.args[0]['M']
    conn.commit()
    conn.close()
    return project


@get_conn
def get_projects(conn: Connection = None, cur: Cursor = None) -> List[Project]:
    """
    Returns all projects from the database.
    """
    cur.execute("SELECT DISTINCT ON (name) id, name, description, version, specification "
                "FROM projects ORDER BY name, version")
    projects = cur.fetchall()
    conn.close()
    return [Project(p[0], p[1], p[2], p[3], p[4]) for p in projects]

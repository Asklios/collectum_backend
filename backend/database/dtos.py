from datetime import datetime


class Data:
    id: int
    timestamp: datetime
    user_id: str
    user_name: str
    project_id: str
    project_version: int
    data_id: int
    data_version: int
    data: dict

    def __init__(self, db_id: int, timestamp: datetime, user_id: str, user_name: str, project_id: str,
                 project_version: int, data_id: int, data_version: int, data: dict):
        self.id = db_id
        self.timestamp = timestamp
        self.user_id = user_id
        self.user_name = user_name
        self.project_id = project_id
        self.project_version = project_version
        self.data_id = data_id
        self.data_version = data_version
        self.data = data

    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            'user_id': self.user_id,
            'user_name': self.user_name,
            'project_id': self.project_id,
            'project_version': self.project_version,
            'data_id': self.data_id,
            'data_version': self.data_version,
            'data': self.data
        }


def data_dto_from_dict(data_json):
    return Data(data_json.get('id'), data_json.get('timestamp'), data_json.get('user_id'), data_json.get('user_name'),
                data_json.get('project_id'), data_json.get('project_version'), data_json.get('data_id'),
                data_json.get('data_version'), data_json.get('data'))


class Project:
    id: int
    name: str
    description: str
    version: int
    specification: dict

    def __init__(self, db_id: int, name: str, description: str, version: int, specification: dict):
        self.id = db_id
        self.name = name
        self.description = description
        self.version = version
        self.specification = specification

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'version': self.version,
            'specification': self.specification
        }


def project_dto_from_dict(project_json):
    return Project(project_json.get('id'), project_json.get('name'), project_json.get('description'),
                   project_json.get('version'), project_json.get('specification'))

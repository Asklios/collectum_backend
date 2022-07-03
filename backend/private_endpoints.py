from flask import request
from flask_restx import Resource, fields, marshal

from api import api
import settings
from auth import check_token
from database import db
from database.dtos import data_dto_from_dict, project_dto_from_dict

namespace = api.namespace('data', description='Private data endpoints')

data_model = api.model(
    'Data',
    {
        "id": fields.Integer(description='Unique identifier'),
        "timestamp": fields.DateTime(required=True, description='Timestamp'),
        "user_id": fields.String(required=True, description='User id'),
        "user_name": fields.String(required=True, description='User name'),
        "project_id": fields.Integer(required=True, description='Project id'),
        "project_version": fields.Integer(required=True, description='Project version'),
        "data_id": fields.Integer(required=True, description='Data id'),
        "data_version": fields.Integer(required=True, description='Data version'),
        "data": fields.Raw(required=True, description='JSON Data')
    }
)

data_model_list = api.model(
    'DataList',
    {
        "data": fields.List(fields.Nested(data_model))
    }
)

project_model = api.model(
    'Project',
    {
        "id": fields.Integer(description='Unique identifier'),
        "name": fields.String(required=True, description='Project name'),
        "description": fields.String(description='Project description'),
        "version": fields.Integer(required=True, description='Project version'),
        "specification": fields.Raw(required=True, description='JSON Project specification')
    }
)

projects_model = api.model(
    'Projects',
    {
        "projects": fields.List(fields.Nested(project_model))
    }
)

project_id = api.model(
    'ProjectId',
    {
        "project_id": fields.Integer(required=True, description='Project id')
    }
)

project_id_data_id = api.model(
    'ProjectIdDataId',
    {
        "project_id": fields.Integer(required=True, description='Project id'),
        "data_id": fields.Integer(required=True, description='Data id')
    }
)


@namespace.route('/')
class Data(Resource):

    @api.doc(body=data_model, security='bearerAuth')
    @api.expect(data_model, validate=True)
    @check_token
    def post(self):
        j = request.json
        data = data_dto_from_dict(j)
        data = db.add_data(data)

        if isinstance(data, str):
            return {'error': data}, 400

        return marshal(data.to_dict(), data_model), 200

    @api.doc(body=data_model_list, security='bearerAuth')
    @api.expect(project_id, validate=True)
    @check_token
    def get(self):
        j = request.json
        project = j.get('project_id')

        if project is None:
            return {'error': 'No project id provided'}, 400

        if not isinstance(project, int):
            return {'error': 'Project id must be an integer'}, 400

        data = db.get_latest_data(project)

        if isinstance(data, str):
            return {'error': data}, 400

        if data is None:
            return {'error': 'No data found for project id {}'.format(project)}, 404

        data = {
            'data': [data.to_dict() for data in data]
        }

        return marshal(data, data_model_list), 200


@namespace.route('/history')
class DataHistory(Resource):

    @api.doc(body=data_model_list, security='bearerAuth')
    @api.expect(project_id_data_id, validate=True)
    @check_token
    def get(self):
        j = request.json

        project = j.get('project_id')
        data_id = j.get('data_id')

        if project is None:
            return {'error': 'No project_id provided'}, 400

        if data_id is None:
            return {'error': 'No data_id provided'}, 400

        if not isinstance(project, int):
            return {'error': 'project_id must be an integer'}, 400

        if not isinstance(data_id, int):
            return {'error': 'data_id must be an integer'}, 400

        data = db.get_data_history(project, data_id)

        if data is None:
            return {'error': 'No data found for project_id {} and data_id {}'.format(project, data_id)}, 404

        data = {
            'data': [data.to_dict() for data in data]
        }

        return marshal(data, data_model_list), 200


@namespace.route('/projects')
class Projects(Resource):

    @api.doc(body=project_model, security='bearerAuth')
    @api.expect(project_model, validate=True)
    @check_token
    def post(self):
        j = request.json
        password = request.headers.get('password')

        if password is None:
            return {'error': "No password provided via header 'password'"}, 401

        if password != settings.API_ADMIN_PASS:
            return {'error': "Invalid password"}, 401

        project = project_dto_from_dict(j)
        project = db.add_project(project)

        if isinstance(project, str):
            return {'error': project}, 400

        return marshal(project.to_dict(), project_model), 200

    @api.doc(body=projects_model, security='bearerAuth')
    @check_token
    def get(self):
        projects = {"projects": [
            project.to_dict() for project in db.get_projects()
        ]}
        return marshal(projects, projects_model), 200

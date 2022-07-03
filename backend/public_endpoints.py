from flask_restx import Resource, fields

import settings
from api import api

namespace = api.namespace('info', description='Open info Endpoints')


health: {str: bool}
health = {
    'db': True
}


identity_provider = api.model(
    'IdentityProvider',
    {
        "client_id": fields.String(required=True, description='The Keycloak client_id'),
        "base_url": fields.String(required=True, description='The Keycloak base_url'),
        "realm": fields.String(required=True, description='The Keycloak realm'),
    }
)


@namespace.route('/health')
class Health(Resource):
    @staticmethod
    def get():
        global health
        if all(health.values()):
            return {'message': 'healthy'}, 200
        else:
            return {'message': health}, 500


@namespace.route('/identity-provider')
class IdentityProvider(Resource):

        @staticmethod
        def get():
            return {
                "client_id": settings.KEYCLOAK_CLIENT_ID,
                "base_url": settings.KEYCLOAK_BASE_URL,
                "realm": settings.KEYCLOAK_REALM,
            }, 200

from flask_restx import Api

import settings

authorizations = {
    'bearerAuth': {
        'type': 'http',
        'scheme': 'basic'
    }
}


api = Api(version='1.0', title='collectum', description='API for the collectum app',
          url_scheme=settings.URL_SCHEME, authorizations=authorizations)


@api.errorhandler
def std_handler():
    return {'message': 'unexpected error'}, 500

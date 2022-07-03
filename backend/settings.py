import os

PORT = os.environ.get('PORT', 5000)
SERVER_NAME = os.environ.get('SERVER_NAME', f'localhost:{PORT}')
URL_SCHEME = os.environ.get('URL_SCHEME', 'http')

RESTPLUS_SWAGGER_EXPANSION = os.environ.get('RESTPLUS_SWAGGER_EXPANSION', 'list')
RESTPLUS_VAL = os.environ.get('RESTPLUS_VAL', True)
RESTPLUS_MASK_SWAGGER = os.environ.get('RESTPLUS_MASK_SWAGGER', False)

RECEIVE_TOKEN = os.environ.get('RECEIVE_TOKEN', 'test_token')
SEND_TOKEN = os.environ.get('SEND_TOKEN', 'test_token')

EXPORT_SWAGGER_FILE = os.environ.get('EXPORT_SWAGGER_FILE') is not None

KEYCLOAK_CLIENT_ID = os.environ.get('KEYCLOAK_CLIENT_ID', 'test_client_id')
KEYCLOAK_BASE_URL = os.environ.get('KEYCLOAK_BASE_URL', 'test_base_url')
KEYCLOAK_REALM = os.environ.get('KEYCLOAK_REALM', 'test_realm')

POSTGRES_URL = os.environ.get('POSTGRES_URL', 'localhost')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', 5432)
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'flask')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'devPa55w0rd')
PG_TIMEZONE = os.environ.get('PG_TIMEZONE', 'Europe/Berlin')

JWT_PUBLIC_KEY = os.environ.get('JWT_PUBLIC_KEY', 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkeY6fsm+VhlcyBtkL6Oi6+6/'
                                                  'z/LTBA5nQ0jnCch8qUrFAJBkk7RITYw+P42wC17ij4oyiyqID9/X2/lbwOp3z7X7Y8JB'
                                                  'etY0mMtGkWh/HPmK5Yk19edTzUqk6LVmY7LXRCTZlhqEmb/YfjFc0I0fJyEflL2BHu8/'
                                                  'hBVOvJDCbiY+d4YimQNyRIlSRLUhbsa3jKlXm5bFcu27nfZMOv1ZLxTLEjBDWQMTuCZ5'
                                                  'hVfZ/41ylSLUNoRXmTamAmJssenzMUi7RN0Q/PE7f+pmEn2qtBj0tC+6YOjY+k6fLQvF'
                                                  'ozU5q1QpUzy+G4Uqo83J55CaPWWyLGVDLVdrQyYFm5XW6wIDAQAB')

API_ADMIN_PASS = os.environ.get('API_ADMIN_PASS', 'devPa55w0rd')

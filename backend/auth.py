import jwt
from flask import request
from flask_restx import reqparse
from jwt import ExpiredSignatureError, DecodeError

from api import api
from settings import JWT_PUBLIC_KEY


class User:
    id: str
    username: str

    def __init__(self, user_id: str, username: str):
        self.id = user_id
        self.username = username

    def __str__(self):
        return f'User: {self.username} ({self.id})'

    def __eq__(self, other):
        if not isinstance(other, User):
            return NotImplemented
        return self.id == other.id, self.username == other.username


def decode_jwt(token: str):
    key = '-----BEGIN PUBLIC KEY-----\n' + JWT_PUBLIC_KEY + "\n-----END PUBLIC KEY-----"
    try:
        payload = jwt.decode(token, key, algorithms=["RS256"], options={
            'verify_aud': False
        })

        user_id = payload['sub']
        user_name = payload['username']

        user = User(user_id, user_name)

        return user
    except ExpiredSignatureError:
        return 'Token signature has expired'
    except DecodeError:
        return 'Token not valid'


access_token_parser = reqparse.RequestParser()
access_token_parser.add_argument('Authorization', type=str, help='Bearer JWT', location='headers')


def check_token(func):
    def inner(self, **args):

        bearer_token = request.headers.get('Authorization')

        if bearer_token is None:
            return {'error': 'missing token'}, 401

        if not bearer_token.startswith('Bearer'):
            return {'error': f"Authorization required in "
                             f"\'{api.authorizations.get('bearerAuth').get('bearerFormat')}\' format"}, 401

        token = bearer_token.split(' ')[1]

        self.user = decode_jwt(token)

        if isinstance(self.user, str):
            return {'error': self.user}, 400

        return func(self, **args)

    return inner

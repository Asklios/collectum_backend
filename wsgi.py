from gevent.pywsgi import WSGIServer
from app import application
from backend.database import db
from backend.settings import *


print('----STARTUP----')
db.init_db()
http_server = WSGIServer(('', PORT), application)
http_server.serve_forever()

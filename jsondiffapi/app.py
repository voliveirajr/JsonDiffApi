from flask import Flask
from flask_restful import Api
from flask_mongoengine import MongoEngine
from resources.diff_resource import *
from logging.config import fileConfig

app = Flask(__name__)

if app.config['ENV'] == 'production':
    app.config['MONGODB_SETTINGS'] = {
        'db': 'diff_db',
        'host': 'mongodb',
        'port': 27017,
    }
else:
    #configuration for tests and development purposes
    app.config['MONGODB_SETTINGS'] = {
        'db': 'diff_db',
        'host': 'localhost',
        'port': 27017,
    }

api = Api(app)
db = MongoEngine(app)

#registering all endpoints
api.add_resource(Diff, '/v1/diff/<id>')
api.add_resource(AddRight, '/v1/diff/<id>/right')
api.add_resource(AddLeft, '/v1/diff/<id>/left')
app.logger.info('Application Started')

if __name__ == '__main__':
    app.run(debug=True)

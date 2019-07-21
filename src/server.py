from flask_restplus import Api

api = Api(
    version='1.0', title='Film Polls API',
)

MovieNamespace = api.namespace('movies', description='Movie actions')

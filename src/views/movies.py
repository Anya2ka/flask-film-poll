import bson
from flask_restplus import Resource, fields, marshal, reqparse

from ..server import MovieNamespace, api
from ..services import movies as MovieService

# Request
MovieRequestModel = api.model('MovieRequest', {
    'title': fields.String(required=True),
    'genres': fields.List(fields.String(), required=True)
})

query_parser = reqparse.RequestParser()
query_parser.add_argument('genre', location='args')

# Response
MovieModel = api.model('Movie', {
    'id': fields.String(required=False, readonly=True, attribute='_id'),
    'title': fields.String(required=True),
    'genres': fields.List(fields.String(), required=True)
})


# Handlers
@MovieNamespace.route('/')
class MoviesList(Resource):
    @MovieNamespace.expect(query_parser)
    @MovieNamespace.marshal_with(MovieModel)
    def get(self):
        data = query_parser.parse_args()
        query = {}

        if data.get('genre'):
            query['genres'] = data['genre']

        return MovieService.find(query)

    @MovieNamespace.expect(MovieRequestModel, validate=True)
    @MovieNamespace.marshal_with(MovieModel)
    def post(self):
        data = marshal(api.payload, MovieRequestModel)

        movie_id = MovieService.create(data)
        return MovieService.find_by_id(movie_id)


@MovieNamespace.route('/<string:movie_id>/')
class MovieDetails(Resource):
    @MovieNamespace.marshal_with(MovieModel)
    def get(self, movie_id):
        try:
            return MovieService.find_by_id(movie_id)
        except (ValueError, bson.errors.InvalidId):
            MovieNamespace.abort(
                404, 'Movie with id \'{}\' not found '.format(movie_id))

    @MovieNamespace.expect(MovieRequestModel)
    @MovieNamespace.marshal_with(MovieModel)
    def patch(self, movie_id):
        try:
            MovieService.update(movie_id, api.payload)
            return MovieService.find_by_id(movie_id)
        except (ValueError, bson.errors.InvalidId):
            MovieNamespace.abort(
                404, 'Movie with id \'{}\' not found '.format(movie_id))

    def delete(self, movie_id):
        try:
            MovieService.delete(movie_id)
            return None, 204
        except (ValueError, bson.errors.InvalidId):
            MovieNamespace.abort(
                404, 'Movie with id \'{}\' not found '.format(movie_id))

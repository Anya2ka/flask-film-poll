import bson
from flask_restplus import Resource, fields, marshal

from ..server import MovieNamespace, api
from ..services import movies as MovieService

# Request
MovieRequestModel = api.model('MovieRequest', {
    'title': fields.String(required=True),
    'genres': fields.List(fields.String(), required=True)
})

# Response
MovieModel = api.model('Movie', {
    '_id': fields.String(required=False, readonly=True),
    'title': fields.String(required=True),
    'genres': fields.List(fields.String(), required=True)
})


# Handlers
@MovieNamespace.route('/')
class MoviesList(Resource):
    @MovieNamespace.marshal_with(MovieModel)
    def get(self):
        return MovieService.find()

    @MovieNamespace.expect(MovieRequestModel, validate=True)
    @MovieNamespace.marshal_with(MovieModel)
    def post(self):
        data = marshal(api.payload, MovieRequestModel)

        _id = MovieService.create(data)
        return MovieService.find_by_id(_id)


@MovieNamespace.route('/<string:pk>/')
class MovieDetails(Resource):
    @MovieNamespace.marshal_with(MovieModel)
    def get(self, pk):
        try:
            return MovieService.find_by_id(pk)
        except (ValueError, bson.errors.InvalidId):
            MovieNamespace.abort(
                404, 'Movie with _id \'{}\' not found '.format(pk))

    @MovieNamespace.expect(MovieRequestModel)
    @MovieNamespace.marshal_with(MovieModel)
    def patch(self, pk):
        try:
            MovieService.update(pk, api.payload)
            return MovieService.find_by_id(pk)
        except (ValueError, bson.errors.InvalidId):
            MovieNamespace.abort(
                404, 'Movie with _id \'{}\' not found '.format(pk))

    def delete(self, pk):
        try:
            MovieService.delete(pk)
            return None, 204
        except (ValueError, bson.errors.InvalidId):
            MovieNamespace.abort(
                404, 'Movie with _id \'{}\' not found '.format(pk))

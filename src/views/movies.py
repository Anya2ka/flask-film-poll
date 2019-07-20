from flask_restplus import Resource, fields, marshal

from ..server import MovieNamespace, api
from ..services import movies as MovieService


# Request
MovieCreateModel = api.model('MovieCreate', {
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

    @MovieNamespace.expect(MovieCreateModel, validate=True)
    @MovieNamespace.marshal_with(MovieModel)
    def post(self):
        data = marshal(api.payload, MovieCreateModel)

        _id = MovieService.create(data)
        return MovieService.find_by_id(str(_id))

import bson
from flask_restplus import Resource, fields, marshal

from ..server import PollNamespace, api
from ..services import polls as PollService


class MovieMask:
    @staticmethod
    def apply(value):
        data = {}

        for key, value in value.items():
            data[key] = len(value)

        return data


# Request
PollRequestModel = api.model('PollRequest', {
    'movies': fields.Raw(example={'<id>': []})
})

# Request
ValueRequestModel = api.model('ValueRequest', {
    'value': fields.Integer(required=True)
})

# Response
PollModel = api.model('Poll', {
    'id': fields.String(required=False, readonly=True, attribute='_id'),
    'movies': fields.Raw(
        mask=MovieMask,
        example={'<id>': 0}
    )
})


# Handlers
@PollNamespace.route('/')
class PollsList(Resource):
    @PollNamespace.marshal_with(PollModel)
    def get(self):
        return PollService.find()

    @PollNamespace.expect(PollRequestModel, validate=True)
    @PollNamespace.marshal_with(PollModel)
    def post(self):
        data = marshal(api.payload, PollRequestModel)

        poll_id = PollService.create(data)
        return PollService.find_by_id(poll_id)


@PollNamespace.route('/<string:poll_id>/')
class PollDetails(Resource):
    @PollNamespace.marshal_with(PollModel)
    def get(self, poll_id):
        try:
            return PollService.find_by_id(poll_id)
        except (ValueError, bson.errors.InvalidId):
            PollNamespace.abort(
                404, 'Poll with id \'{}\' not found '.format(poll_id))

    @PollNamespace.expect(PollRequestModel)
    @PollNamespace.marshal_with(PollModel)
    def patch(self, poll_id):
        try:
            PollService.update(poll_id, api.payload)
            return PollService.find_by_id(poll_id)
        except (ValueError, bson.errors.InvalidId):
            PollNamespace.abort(
                404, 'Poll with id \'{}\' not found '.format(poll_id))

    def delete(self, poll_id):
        try:
            PollService.delete(poll_id)
            return None, 204
        except (ValueError, bson.errors.InvalidId):
            PollNamespace.abort(
                404, 'Poll with id \'{}\' not found '.format(poll_id))


@PollNamespace.route('/<string:poll_id>/<string:movie_id>/')
class MovieValue(Resource):
    @PollNamespace.expect(ValueRequestModel)
    @PollNamespace.marshal_with(PollModel)
    def post(self, poll_id, movie_id):
        data = api.payload["value"]
        if data < 1 or data > 10:
            PollNamespace.abort(
                400, "Unsupported value")
        try:
            PollService.update_by_details(poll_id, movie_id, data)
            return PollService.find_by_id(poll_id)
        except ValueError as error:
            PollNamespace.abort(404, error.args[0])
        except bson.errors.InvalidId as error:
            PollNamespace.abort(400, error.args[0])

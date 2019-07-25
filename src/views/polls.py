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

# Response
PollModel = api.model('Poll', {
    '_id': fields.String(required=False, readonly=True),
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

        _id = PollService.create(data)
        return PollService.find_by_id(_id)


@PollNamespace.route('/<string:pk>/')
class PollDetails(Resource):
    @PollNamespace.marshal_with(PollModel)
    def get(self, pk):
        try:
            return PollService.find_by_id(pk)
        except (ValueError, bson.errors.InvalidId):
            PollNamespace.abort(
                404, 'Poll with _id \'{}\' not found '.format(pk))

    @PollNamespace.expect(PollRequestModel)
    @PollNamespace.marshal_with(PollModel)
    def patch(self, pk):
        try:
            PollService.update(pk, api.payload)
            return PollService.find_by_id(pk)
        except (ValueError, bson.errors.InvalidId):
            PollNamespace.abort(
                404, 'Poll with _id \'{}\' not found '.format(pk))

    def delete(self, pk):
        try:
            PollService.delete(pk)
            return None, 204
        except (ValueError, bson.errors.InvalidId):
            PollNamespace.abort(
                404, 'Poll with _id \'{}\' not found '.format(pk))

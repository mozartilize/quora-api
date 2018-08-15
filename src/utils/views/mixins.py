from flask import request
from marshmallow.exceptions import ValidationError
from utils.decorators import hashids_decode


class ResourceCreationMixin:
    def get_post_schema_class(self):
        return self.post_schema_class

    def get_schema_args(self):
        return {}

    def get_schema(self):
        return self.get_schema_class()(**self.get_schema_args())

    def get_created_resource_url(self, id):
        raise NotImplementedError

    def persist_record(self, data):
        raise NotImplementedError

    @hashids_decode()
    def post(self, *args, **kwargs):
        schema = self.get_schema()
        try:
            payload = request.form or request.json
            data = schema.load(payload)
            instance = self.persist_record(data)
            return {'id': instance.id}, \
                201, \
                {'Location': self.get_created_resource_url(instance.id)}
        except ValidationError as e:
            return {'message': '', 'errors': e.messages}, 400


class SingleResourceDetailMixin:
    @hashids_decode()
    def get(self, *args, **kwargs):
        return {'id': kwargs['id']}

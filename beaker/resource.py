import json
from werkzeug.routing import Rule
from werkzeug.wrappers import Request, Response

__all__ = ['Resource']


class ResourceMetaClass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Resource':
            return type.__new__(cls, name, bases, attrs)
        attrs['rules'] = [
            Rule('/{}s'.format(name.lower()), endpoint=name),
            Rule(
                '/{}s/<{}_id>'.format(name.lower(), name.lower()),
                endpoint=name)]
        if bases[0].__name__ is not 'Resource':
            attrs['rules'] = [
                Rule('/{}s/<{}_id>/{}s'.format(
                    bases[0].__name__.lower(),
                    bases[0].__name__.lower(),
                    name.lower()), endpoint=name),
                Rule(
                    '/{}s/<{}_id>'.format(name.lower(), name.lower()),
                    endpoint=name)]

        return type.__new__(cls, name, bases, attrs)


class Resource(object):
    """docstring for Home"""

    __metaclass__ = ResourceMetaClass

    def __init__(self, request, endpoint, values):
        super(Resource, self).__init__()
        self.request = request
        self.endpoint = endpoint
        self.values = values

    def dispatch_request(self, request):
        func_method_map = {
            'get': 'get',
            'update': 'put',
            'delete': 'delete'
        }

        resource_id = '{}_id'.format(self.__class__.__name__.lower())
        if request.method.lower() == 'get'\
                and resource_id not in self.values.keys():
            return getattr(self, 'query', None)(**self.values)
        if request.method.lower() == 'post'\
                and resource_id not in self.values.keys():
            return getattr(self, 'save', None)(**self.values)
        resp = getattr(
            self,
            func_method_map.get(request.method.lower()),
            None)(**self.values)
        if isinstance(resp, Response):
            return resp
        elif isinstance(resp, dict):
            return Response(json.dumps(resp))

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

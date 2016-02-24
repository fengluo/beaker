import json
from werkzeug.routing import Rule
from werkzeug.wrappers import Request, Response

__all__ = ['Resource']


class ResourceMetaClass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Resource':
            return type.__new__(cls, name, bases, attrs)
        if not attrs.get('__resource__'):
            attrs['__resource__'] = '{}s'.format(name.lower())
        if not attrs.get('__resource_id__'):
            attrs['__resource_id__'] = '{}_id'.format(name.lower())

        attrs['rules'] = [
            Rule(
                '/{}/<{}>'.format(
                    attrs['__resource__'], attrs['__resource_id__']),
                endpoint=name)]

        parent_resource = next(
            (base for base in bases
                if isinstance(base, cls) and base.__name__ is not 'Resource'),
            None)

        if parent_resource:
            attrs['rules'].append(
                Rule('/{}/<{}>/{}'.format(
                    parent_resource.__resource__,
                    parent_resource.__resource_id__,
                    attrs['__resource__']), endpoint=name))
        else:
            attrs['rules'].append(
                Rule('/{}'.format(attrs['__resource__']), endpoint=name))

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

        if request.method.lower() == 'get'\
                and self.__resource_id__ not in self.values.keys():
            return getattr(self, 'query', None)(**self.values)
        if request.method.lower() == 'post'\
                and self.__resource_id__ not in self.values.keys():
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

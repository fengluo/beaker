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
        self.req = request
        self.endpoint = endpoint
        self.values = values
        self.resp = Resp()

    def dispatch_request(self, request):
        func_method_map = {
            'show': 'get',
            'update': 'put',
            'destroy': 'delete'
        }

        if request.method.lower() == 'get'\
                and self.__resource_id__ not in self.values.keys():
            return getattr(self, 'index', None)(**self.values)
        if request.method.lower() == 'post'\
                and self.__resource_id__ not in self.values.keys():
            return getattr(self, 'create', None)(**self.values)
        resp = getattr(
            self,
            func_method_map.get(request.method.lower()),
            None)(**self.values)
        return resp

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)


class JSONResp(object):

    def json(self, data):
        self.headers['Content-Type'] = 'application/json; charset=UTF-8'
        self.set_data(json.dumps(data))
        return self


class HTMLResp(object):

    def html(self, template_name, **context):
        pass


class Resp(Response, JSONResp):
    """Full featured response object"""

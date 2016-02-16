import pkgutil
import inspect
from werkzeug.wrappers import Request
from werkzeug.routing import Map

from .resource import Resource


def import_all_module(name, modules=None):
    modules = modules if modules is not None else []
    package = __import__(name, fromlist="dummy")
    prefix = package.__name__ + "."
    for imp, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix):
        if not ispkg:
            modules.append(__import__(modname, fromlist="dummy"))
        else:
            modules = import_all_module(modname, modules)
    return modules


class App(object):

    def __init__(self, name=__name__):
        modules = import_all_module(name)
        self.rules = []
        self.views = []
        for module in modules:
            for k, v in module.__dict__.items():
                if inspect.isclass(v) and issubclass(v, Resource)\
                        and v is not Resource:
                    self.rules.extend(v.rules)
                    if module not in self.views:
                        self.views.append(module)
        self.url_map = Map(self.rules)

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        endpoint, values = adapter.match()
        for view in self.views:
            if hasattr(view, endpoint):
                return getattr(view, endpoint)(request, endpoint, values)

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

import re


class HTTPMethodOverrideMiddleware(object):
    allowed_methods = frozenset([
        'GET',
        'HEAD',
        'POST',
        'DELETE',
        'PUT',
        'PATCH',
        'OPTIONS'
    ])
    bodyless_methods = frozenset(['GET', 'HEAD', 'OPTIONS', 'DELETE'])

    def __init__(self, app, field='_method'):
        self.app = app
        self._regex = re.compile('.*' + field + '=([a-zA-Z]+)(&.*|$)')

    def __call__(self, environ, start_response):
        method = self._regex.match(environ.get('QUERY_STRING', ''))
        if method is not None:
            method = method.group(1).upper()
            if method in self.allowed_methods:
                environ['REQUEST_METHOD'] = method
            if method in self.bodyless_methods:
                environ['CONTENT_LENGTH'] = '0'
        return self.app(environ, start_response)

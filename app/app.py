from pprint import pformat


def hello(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    yield b'Hello world!'


def application(env, start_response):
    status = '200 ok'
    get_params = env['QUERY_STRING'].encode('utf-8')
    query_string_args = dict([_.split('=') for _ in get_params.decode('utf-8').split('&')])

    l = int(env.get('CONTENT_LENGTH')) if env.get('CONTENT_LENGTH') else 0
    post_params = env['wsgi.input'].read(l) if l > 0 else ''

    if query_string_args["mode"] == "get":
        headers = [
            ('Content-Type', 'text/plain'),
            ('Content-Length', str(len(str(query_string_args).encode('utf-8')))),
        ]
        start_response(status, headers)
        yield str(query_string_args).encode('utf-8')

    elif query_string_args["mode"] == "post":
        headers = [
            ('Content-Type', 'text/plain'),
            ('Content-Length', str(len(post_params))),
        ]
        start_response(status, headers)
        yield post_params

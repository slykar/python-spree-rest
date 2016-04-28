from .utils import get_from_settings, get_option_list

OPTION_HEADERS = {
    'origins': 'Access-Control-Allow-Origin',
    'headers': 'Access-Control-Allow-Headers',
    'credentials': 'Access-Control-Allow-Credentials',
    'max_age': 'Access-Control-Max-Age'
}


def apply_cors(request, response):
    """
    Apply cors policy headers on the response
    :type request: pyramid.request.Request
    :param response:
    :return:
    """
    settings = get_from_settings(request.registry.settings)

    if 'headers' in settings:
        settings['headers'] = ', '.join(get_option_list(settings, 'headers'))

    headers = {OPTION_HEADERS[key]: settings[key] for key in settings}
    response.headers.update(headers)

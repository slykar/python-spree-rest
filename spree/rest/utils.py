def get_from_settings(settings, prefix='cors.', **kwargs):
    """
    Get settings `dict` with keys starting with `prefix`
    :param settings: settings dictionary
    :type settings: dict
    :param prefix: key prefix
    :type prefix: str
    :param kwargs: override settings
    :type kwargs: dict
    :return: extracted settings dict
    :rtype: dict
    """
    options = {
        key[len(prefix):]: settings[key]
        for key in settings
        if key.startswith(prefix)
    }
    options.update(kwargs)
    return options


def get_option_list(settings, key, default=None):
    """
    Return string `settings` value as `list` split by lines
    :param settings: settings dictionary
    :param key: dictionary key
    :param default: default value if `key` is not in `settings`
    :return: settings value
    :rtype: str|list[str]
    """
    if key not in settings:
        return default

    value = settings[key]
    lines = value.splitlines()
    return list(filter(None, lines))

def get_from_settings(settings, prefix='cors.', **kwargs):
    options = {
        key[len(prefix):]: settings[key]
        for key in settings
        if key.startswith(prefix)
    }
    options.update(kwargs)
    return options


def get_option_list(settings, key, default=None):
    if key not in settings:
        return default

    value = settings[key]
    lines = value.splitlines()
    return list(filter(None, lines))

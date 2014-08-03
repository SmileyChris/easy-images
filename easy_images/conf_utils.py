from django.conf import BaseSettings, settings as project_settings


class SettingDict(object):
    """
    A group of settings which can be individually overridden in a dictionary
    in the project's settings module.

    Use a subclass of this object, defining the default settings as attributes.
    """


class AppSettings(BaseSettings):
    """
    A holder for app-specific settings.

    The holder returns attributes from the project's setting module, falling
    back to the default attributes provided in this module if the attribute
    wasn't found.
    """
    def __init__(self, *args, **kwargs):
        super(AppSettings, self).__init__(*args, **kwargs)
        self.__dicts = {}

    def __getattribute__(self, attr):
        try:
            return self.__dicts[attr]
        except KeyError:
            pass
        try:
            project_value = getattr(project_settings, attr)
            if not isinstance(project_value, dict):
                return project_value
        except AttributeError:
            project_value = None

        value = super(AppSettings, self).__getattribute__(attr)

        if project_value is None:
            return value

        if issubclass(value, SettingDict):
            value = dict([
                (k, v) for k, v in value.__dict__.items()
                if not k.startswith('_')])
            value.extend(project_value)
            project_value = value
        self.__dicts[attr] = project_value
        return project_value

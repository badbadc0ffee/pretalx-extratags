from django.apps import AppConfig


class PluginApp(AppConfig):
    name = "pretalx_extratags"

    class PretalxPluginMeta:
        name = "Extra E-Mail Tags"
        author = "Florian Mösch"
        description = "Ein zusätzliches E-Mail-Tag für Schedule-Benachrichtigungen."
        version = "0.8.15"
        category = "FEATURE"

    def ready(self):
        from . import signals  # noqa: F401

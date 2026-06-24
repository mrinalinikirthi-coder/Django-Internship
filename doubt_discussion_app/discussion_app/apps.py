from django.apps import AppConfig


class DiscussionConfig(AppConfig):
    name = 'discussion_app'

    def ready(self):
        from . import signals  # noqa: F401

from django.apps import AppConfig


class DiscussionConfig(AppConfig):
    name = 'discussion-app'

    def ready(self):
        import discussion.signals

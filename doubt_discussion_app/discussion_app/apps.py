"""
App configuration for the Discussion App.

This module defines the application configuration and handles
the initialization of app-specific components like signals.
"""

from django.apps import AppConfig


class DiscussionConfig(AppConfig):
    """
    Configuration class for the Discussion application.

    This class registers the app with Django and ensures that
    signals are loaded when the app is ready.
    """

    # The full Python path to the application
    name = 'discussion_app'

    def ready(self):
        """
        Hook to run when the application is ready.

        This method is called when Django finishes loading the app.
        It imports the signals module to connect signal handlers,
        ensuring that all signal receivers are registered.
        """
        # Import signals to register all signal handlers
        # The # noqa: F401 comment tells Flake8 to ignore
        # "unused import" warning
        from . import signals  # noqa: F401

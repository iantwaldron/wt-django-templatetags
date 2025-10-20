from django.templatetags.static import StaticNode
from django import template

import wt_templatetags.settings as settings


register = template.Library()


def make_min(path):
    """
    Transform a static file path to use the minified version.

    Checks if the path ends with any extension in STATIC_MIN_EXTENSIONS,
    and if so, inserts STATIC_MIN_SUFFIX before the extension.

    Args:
        path (str): The static file path to transform (e.g., "/static/css/main.css")

    Returns:
        str: The transformed path with minified suffix inserted
             (e.g., "/static/css/main.min.css"), or the original path if
             no matching extension is found.

    Raises:
        ValueError: If no matching extension is found and
                    STATIC_MIN_FAIL_SILENT is False.
    """

    for ext in settings.STATIC_MIN_EXTENSIONS:
        if path.endswith(ext):
            path = path.replace(ext, f'.{settings.STATIC_MIN_SUFFIX}{ext}')
            break
    else:
        if not settings.STATIC_MIN_FAIL_SILENT:
            raise ValueError(f"No matching extension for path '{path}' with "
                             f"extensions '{', '.join(settings.STATIC_MIN_EXTENSIONS)}")

    return path


class StaticMinNode(StaticNode):
    """
    StaticNode subclass that transforms paths to use minified files.
    """

    @classmethod
    def handle_simple(cls, path):
        path = super().handle_simple(path)
        return make_min(path)


@register.tag
def static_min(parser, token):
    """
    Extends Django 'static' template tag to transform path to use minified
       files (e.g., '.css' becomes '.min.css').

    Usage::

        {% static path [as varname] %}
        {# same as Django usage #}
    """
    return StaticMinNode.handle_token(parser, token)

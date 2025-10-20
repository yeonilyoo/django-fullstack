from django import template
from django.conf import settings

register = template.Library()


@register.filter()
def strip_lang_prefix(path):
    # assume LANGUAGE_CODE is 2 letters
    if path[:3] in [f"/{lang}" for lang, _ in settings.LANGUAGES]:
        return path[3:] or "/"  # return "/" if path becomes empty
    return path


@register.filter
def is_lang(request, lang_code):
    if hasattr(request, "LANGUAGE_CODE"):
        # only compare first 2 characters (en-us -> en)
        return request.LANGUAGE_CODE[:2] == lang_code
    return False

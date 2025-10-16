import markdown
from django import template

# 장고 이스케이프에서 안전한 html 태그로 렌더링 하기 위해 필요
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def sub(value, arg):
    return value - arg


@register.filter()
def mark(value):
    extensions = ["extra", "nl2br", "fenced_code", "sane_lists"]
    return mark_safe(markdown.markdown(value, extensions=extensions))


@register.filter
def category_badge_class(category):
    return {
        "question": "badge-info",
        "free": "badge-success",
        "lecture": "badge-warning",
    }.get(category, "badge-secondary")

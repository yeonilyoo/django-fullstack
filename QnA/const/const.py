from django.utils.translation import gettext_lazy as _

CATEGORY_CHOICE = [
    ("question", _("QUESTION.CATEGORY.QUESTION")),
    ("free", _("QUESTION.CATEGORY.FREE")),
    ("lecture", _("QUESTION.CATEGORY.LECTURE")),
]

CATEGORY_ALL_CHOICE = [("all", _("QUESTION.CATEGORY.ALL")), *CATEGORY_CHOICE]

# Exclude keyword filter for search
SEARCH_KW_FILTER_LIST = [
    "password",
    "first_name",
    "last_name",
    "email",
    "phone",
    "address",
    "category",
]

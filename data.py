import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.utils import timezone
from pybo.models import Question, Answer
from common.models import User
from pybo.const.const import CATEGORY_CHOICE


if __name__ == "__main__":

    u = User.objects.get(username="user1")
    for i in range(300):
        q = Question(
            subject="Test Data:[%03d]" % i,
            content="Test Data Content:[%03d]" % i,
            create_date=timezone.now(),
            author=u,
            category=CATEGORY_CHOICE[0][0],
        )
        q.save()

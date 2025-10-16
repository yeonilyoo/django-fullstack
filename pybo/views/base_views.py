from functools import reduce
import operator

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count

from ..const.const import CATEGORY_ALL_CHOICE, SEARCH_KW_FILTER_LIST
from ..models import Question, Answer
from ..util.tools import get_string_fields


def index(request):
    # 1 is fallback in case no page is present.
    # page is pulled from url page= and we can nav via this way
    page = request.GET.get("page", "1")
    # search
    kw = request.GET.get("kw", "")
    # sort order
    so = request.GET.get("so", "")
    # category filter
    ca = request.GET.get("ca", "all")

    # question_list = Question.objects.order_by("-create_date")
    if so == "recommend":
        question_list = Question.objects.annotate(num_voter=Count("voter")).order_by(
            "-num_voter", "-create_date"
        )
    elif so == "popular":
        question_list = Question.objects.annotate(num_answer=Count("answer")).order_by(
            "-num_answer", "-create_date"
        )
    else:
        question_list = Question.objects.order_by("-create_date")

    if ca != "all":
        question_list = question_list.filter(category=ca)

    if kw:
        # question_list = question_list.filter(
        #     Q(subject__icontains=kw)
        #     | Q(content__icontains=kw)
        #     | Q(author__username__icontains=kw)
        #     | Q(answer__content__icontains=kw)
        #     | Q(answer__author__username__icontains=kw)
        # ).distinct()
        question_fields = get_string_fields(
            model=Question, filter=SEARCH_KW_FILTER_LIST, depth=2
        )
        # print(question_fields)
        query = reduce(
            operator.or_,
            (Q(**{f"{field}__icontains": kw}) for field in question_fields),
        )
        question_list = question_list.filter(query).distinct()

    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    current_page = page_obj.number
    start_index = max(current_page - 5, 1)
    end_index = min(current_page + 5, paginator.num_pages)
    page_range = range(start_index, end_index + 1)

    context = {
        "question_list": page_obj,
        "page_range": page_range,
        "page": page,
        "kw": kw,
        "so": so,
        "category": CATEGORY_ALL_CHOICE,
        "ca": ca,
    }
    return render(request, "pybo/question_list.html", context)


def detail(request, question_id):
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)

    page = request.GET.get("page", "1")
    kw = request.GET.get("kw", "")
    so = request.GET.get("so", "")

    if so == "old":
        answer_list = question.answer_set.order_by("create_date")
    elif so == "popular":
        answer_list = question.answer_set.annotate(num_voter=Count("voter")).order_by(
            "-num_voter", "-create_date"
        )
    else:
        answer_list = question.answer_set.order_by("-create_date")

    if kw:
        answer_list = answer_list.filter(
            Q(content__icontains=kw) | Q(author__username__icontains=kw),
        ).distinct()

    paginator = Paginator(answer_list, 5)
    page_obj = paginator.get_page(page)

    current_page = page_obj.number
    start_index = max(current_page - 5, 1)
    end_index = min(current_page + 5, paginator.num_pages)
    page_range = range(start_index, end_index + 1)

    if (
        request.user.is_authenticated
        and not question.viewer.filter(id=request.user.id).exists()
    ):
        question.viewer.add(request.user)

    context = {
        "question": question,
        "answer_list": answer_list,
        "page_range": page_range,
        "page": page,
        "kw": kw,
        "so": so,
    }
    return render(request, "pybo/question_detail.html", context)

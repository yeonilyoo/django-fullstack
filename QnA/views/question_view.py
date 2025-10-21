from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse

from api.serializer import QuestionSerializer
from ..forms import QuestionForm
from ..models import Question


@login_required(login_url="common:login")
def question_create_view(request):
    form = QuestionForm()
    context = {"form": form}

    return render(request, "QnA/question_form.html", context)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def question_create(request):
    serializer = QuestionSerializer(data=request.data)
    if serializer.is_valid():
        question = serializer.save(author=request.user, create_date=timezone.now())
        return Response({"id": question.id}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def question_modify(request, question_id):
    question = Question.objects.get(id=question_id)

    if request.user != question.author:
        return Response({"detail", "unauthorized"}, status=status.HTTP_403_FORBIDDEN)

    serializer = QuestionSerializer(data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save(modify_date=timezone.now())
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def question_delete(request, question_id):
    question = Question.objects.get(id=question_id)
    if request.user != question.author:
        return Response({"detail", "unauthorized"}, status=status.HTTP_403_FORBIDDEN)

    question.delete()
    detail_url = reverse("index", request=request)
    headers = {"Location": detail_url}
    return Response(
        {"index": "deleted"}, status=status.HTTP_204_NO_CONTENT, headers=headers
    )

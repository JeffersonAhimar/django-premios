from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import Count

from .models import Question, Choice

# Create your views here.
'''
def index(request):
    latest_question_list = Question.objects.all()
    return render(request, "polls/index.html", {
        "latest_question_list": latest_question_list
    })

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {
        "question": question
    })
    
def results(request, question_id):
    question=get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {
        "question": question
    })
'''
# class
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        '''Return the last five published questions, that have at least two choices'''
        question = Question.objects.filter(pub_date__lte=timezone.now())
        question = question.alias(entries=Count("choice")).filter(entries__gte=2)
        return question.order_by("-pub_date")[:5]  # lte = less than or equal to


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        '''Excludes any question that aren't published yet'''
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultView(DetailView):
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html",{
            "question": question,
            "error_message": "No elegiste una respuesta"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))
        #return redirect("polls:results", question_id)  #shortcut

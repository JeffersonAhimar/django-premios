import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question

# Create your tests here.
class QuestionModelTests(TestCase):

    def setUp(self):
        self.question = Question(question_text="¿Quién es el mejor Course Director?")

    def test_was_published_recently_with_future_questions(self):
        """was_published_recently returns False for questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        self.question.pub_date=time
        self.assertIs(self.question.was_published_recently(), False)

    def test_was_published_recently_with_past_questions(self):
        """was_published_recently returns False for questions whose pub_date is in the past"""
        time = timezone.now() - datetime.timedelta(days=1, minutes=1)
        self.question.pub_date=time
        self.assertIs(self.question.was_published_recently(), False)
    
    def test_was_published_recently_with_present_questions(self):
        """was_published_recently returns True for questions whose pub_date is in the present"""
        time = timezone.now() - datetime.timedelta(hours=23)
        self.question.pub_date=time
        self.assertIs(self.question.was_published_recently(), True)
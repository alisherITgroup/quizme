from django.db import models
from django.contrib.auth.models import User
from random import choice

def generate_token():
    token = ""
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digits = "0123456789"
    for i in range(5):
        token += choice(letters)
        token += choice(digits)
    return token

TYPE = (
    ("private", "Yashirin"),
    ("public", "Ommanviy"),
)

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    question = models.TextField()
    subject = models.CharField(max_length=20)
    type = models.CharField(max_length=20, choices=TYPE)
    
    answer1 = models.TextField()
    answer2 = models.TextField()
    answer3 = models.TextField()
    answer4 = models.TextField()

    correct = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question
    
    def name(self):
        return self.question[:15] + "..."


class Quiz(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=20, choices=TYPE)

    startdate = models.CharField(max_length=20)
    starttime = models.CharField(max_length=20)
    enddate = models.CharField(max_length=20)
    endtime = models.CharField(max_length=20)
    password = models.CharField(max_length=20, default=generate_token, editable=False)
    token = models.CharField(max_length=50, default=generate_token, editable=False)

    questions = models.ManyToManyField(Question, related_name="quiz_questions")
    users = models.ManyToManyField(User, related_name="quiz_users")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def count_users(self):
        return self.users.count()
    
    def count_questions(self):
        return self.questions.count()
    
class Rating(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField(default=0)
    cases = models.TextField(default="{}")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

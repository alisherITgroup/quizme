from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path("", home, name='home'),
    path("login/", login_, name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),

    path("create_question/", create_question, name="create_question"),
    path("questions/", questions, name="questions"),
    path("edit_question/<int:pk>/", edit_question, name="edit_question"),
    path("quizzes/", quizzes, name="quizzes"),
    path("create_quiz/", create_quiz, name="create_quiz"),
    path("quiz/<int:pk>/", quiz, name="quiz"),
    path("add_question/<int:pk>/", add_question, name="add_question"),
    path("test/<str:token>/", test, name="test"),
    path("test/<str:token>/results/", results, name="results")
]
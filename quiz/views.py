from django.shortcuts import render, redirect
from .models import Question, Quiz, Rating
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from random import choice


def login_(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.constants.SUCCESS, "Tizimga kirish muvaqqiyatli amalga oshirildi!")
            messages.add_message(request, messages.constants.SUCCESS, "AlgorithmsHub ga xush kelibsiz!")
            return redirect("home")
        else:
            messages.add_message(request, messages.constants.ERROR, "Foydalanuvchi nomi yoki kalit so'z xato!(Iltimos qayta urinib ko'ring) :(")
    return render(request, "login.html")

def generate():
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digits = "0123456789"
    password = ""
    for i in range(4):
        password += choice(letters)
        password += choice(digits)
    return password

def home(request):
    if request.user.is_superuser:
        user = request.user
        questions = Question.objects.all().filter(author=user)
        quizzes = Quiz.objects.all().filter(author=user)
        ratings = Rating.objects.all().filter(author=request.user)
        return render(
            request,
            "home.html",
            {
                "questions": questions,
                "quizzes": quizzes,
                "homestatus": "active",
                "ratings": ratings
            }
        )
    if request.method == "POST":
        f_name = request.POST.get("f_name")
        l_name = request.POST.get("l_name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        password = generate()
        try:
            user = User.objects.create_user(
                first_name=f_name,
                last_name=l_name,
                email=email,
                username=email,
                password=password
            )
            user.save()
            return render(request, "home.html", {
                "generated": True,
                "username": email,
                "password": password
            })
        except Exception as e:
            return render(request, "home.html", {"generated": False, "error": f"Kechirasiz! {email} bu nom band!"})
    if request.user.is_authenticated:
        ratings = Rating.objects.all().filter(author=request.user)
        quizzes = Quiz.objects.all().filter(type="public").order_by("-id")
        return render(request, "home.html", {"homestatus": "active", "ratings": ratings, "quizzes": quizzes})
    return render(request, "home.html", {"homestatus": "active", "generated": False})

@login_required(login_url="login")
def questions(request):
    if request.user.is_superuser:
        user = request.user
        questions = Question.objects.all().filter(author=user).order_by("-id")
        quizzes = Quiz.objects.all().filter(author=user)
        return render(
            request,
            "questions.html",
            {
                "questions": questions,
                "quizzes": quizzes,
                "questionstatus": "active"
            }
        )
    else:
        return render(request, "404.html")

@login_required(login_url="login")
def create_question(request):
    if request.user.is_superuser:
        if request.method == "POST":
            q = request.POST.get("question")
            answer1 = request.POST.get("answer1")
            answer2 = request.POST.get("answer2")
            answer3 = request.POST.get("answer3")
            answer4 = request.POST.get("answer4")
            correct = request.POST.get("correct")
            subject = request.POST.get("subject")
            type_ = request.POST.get("type")
            if correct in [answer1, answer2, answer3, answer4]:
                question = Question(
                    author=request.user,
                    question=q,
                    answer1=answer1,
                    answer2=answer2,
                    answer3=answer3,
                    answer4=answer4,
                    type=type_,
                    subject=subject,
                    correct=correct
                )
                question.save()
        return HttpResponseRedirect(reverse_lazy("questions"))
    else:
        return render(request, "404.html")

@login_required(login_url="login")
def edit_question(request, pk):
    if request.user.is_superuser:
        question = Question.objects.get(id=pk)
        error = None
        success = None
        if request.method == "POST":
            question.question = request.POST.get("question")
            question.answer1 = request.POST.get("answer1")
            question.answer2 = request.POST.get("answer2")
            question.answer3 = request.POST.get("answer3")
            question.answer4 = request.POST.get("answer4")
            question.correct = request.POST.get("correct")
            if request.POST.get("correct") in [request.POST.get("answer1"), request.POST.get("answer2"), request.POST.get("answer3"), request.POST.get("answer4")]:
                question.save()
                success = "Ajoyib! Savol muvaffaqqiyatli tahrirlandi."
            else:
                error = "Kechirasiz! <b>To'g'ri javob</b> <b>Javob</b>lar ichida bo'lishi kerak."
        return render(request, "edit_question.html", {
            "question": question.question,
            "answer1": question.answer1,
            "answer2": question.answer2,
            "answer3": question.answer3,
            "answer4": question.answer4,
            "correct": question.correct,
            "type": question.type,
            "error": error,
            "success": success,
            "questionstatus": "active"
        })
    else:
        return render(request, "404.html")

@login_required(login_url="login")
def create_quiz(request):
    if request.user.is_superuser:
        if request.method == "POST":
            name = request.POST.get("name")
            type_ = request.POST.get("type")
            startdate = request.POST.get("startdate")
            starttime = request.POST.get("starttime")
            enddate = request.POST.get("enddate")
            endtime = request.POST.get("endtime")
            desc = request.POST.get("description")
            quiz = Quiz(
                author=request.user,
                name=name,
                startdate=startdate,
                starttime=starttime,
                enddate=enddate,
                endtime=endtime,
                type=type_,
                description=desc
            )
            quiz.save()
            return HttpResponseRedirect(reverse("quiz", args=[quiz.id]))
        return HttpResponseRedirect(reverse_lazy("quizzes"))
    else:
        return render(request, "404.html")

@login_required(login_url="login")
def quiz(request, pk):
    if request.user.is_superuser:
        quiz = Quiz.objects.get(id=pk)
        return render(request, "quiz.html", {
            "quiz": quiz,
            "questions": quiz.questions.all()
        })
    return render(request, "404.html")

@login_required(login_url="login")
def quizzes(request):
    if request.user.is_superuser:
        user = request.user
        quizzes = Quiz.objects.all().filter(author=user)
        return render(request, "quizzes.html", {
            "quizzes": quizzes
        })
    else:
        return render(request, "404.html")

@login_required(login_url="login")
def add_question(request, pk):
    if request.user.is_superuser:
        quiz = Quiz.objects.get(id=pk)
        questions = Question.objects.all().filter(author=request.user)
        if request.method == "POST":
            data = dict(request.POST)
            data.pop("csrfmiddlewaretoken")
            for question in data:
                question = Question.objects.get(id=question)
                quiz.questions.add(question)
        quiz.save()
        return render(request, "add_question.html", {
            "quiz": quiz,
            "questions": questions
        })
    else:
        return render(request, "404.html")

@login_required(login_url="login")
def test(request, token):
    quiz = Quiz.objects.get(token=token)
    questions = quiz.questions.all()
    rating = Rating.objects.all().filter(author=request.user, quiz=quiz).first()
    if request.method == "POST":
        data = dict(request.POST)
        data.pop("csrfmiddlewaretoken")
        score = 0
        count = 0
        cases = {}
        i = 1
        percent = round((1/quiz.questions.count())*100, 2)
        for answer, correct in zip(data, questions):
            if (data[answer][0] == correct.correct):
                score += percent
                count += 1
                cases[f"answer{i}"] = "✅"
            else:
                cases[f"answer{i}"] = "❌"
            i += 1
        if rating:
            pass
        else:
            rating = Rating(author=request.user, quiz=quiz)
        rating.score = round(score, 2)
        cases["count"] = count
        rating.cases = str(cases)
        rating.save()
        cases.pop("count")
        return render(request, "test.html", {
            "quiz": quiz,
            "questions": quiz.questions.all(),
            "rating": rating,
            "cases": eval(str(cases)).values()
        })
    cases = list(eval(rating.cases).values()) if rating else [1]
    cases.pop()
    return render(request, "test.html", {
        "quiz": quiz,
        "questions": quiz.questions.all(),
        "rating": rating,
        "cases": cases
    })
   
def results(request, token):
    quiz = Quiz.objects.get(token=token)
    results = Rating.objects.all().filter(quiz=quiz).order_by("-score")
    return render(request, "results.html", {"results": results})
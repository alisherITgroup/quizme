from django.contrib import admin
from .models import Question, Quiz, Rating

@admin.register(Quiz)
class QuizModelAdmin(admin.ModelAdmin):
    list_display = ["token", "name", "author", "count_questions", "count_users"]

@admin.register(Question)
class QuestionModelAdmin(admin.ModelAdmin):
    list_display = ["name", "subject", "type"]

@admin.register(Rating)
class RatingModelAdmin(admin.ModelAdmin):
    list_display  = ["author", "quiz", "score"]
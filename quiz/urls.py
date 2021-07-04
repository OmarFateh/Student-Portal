from django.urls import path

from .views import add_quiz, add_question, quiz_detail, take_quiz, attempt_detail 

# namespace = quiz

urlpatterns = [
    path('courses/<slug:course_slug>/quiz/<int:quiz_id>/', quiz_detail, name='quiz-detail'),
    # Teacher
    path('courses/<slug:course_slug>/<int:module_id>/quiz/add/', add_quiz, name='add-quiz'),
    path('courses/<slug:course_slug>/quiz/<int:quiz_id>/question/add/', add_question, name='add-question'),
    # Student
    path('courses/<slug:course_slug>/quiz/<int:quiz_id>/take/', take_quiz, name='take-quiz'),
    path('courses/<slug:course_slug>/quiz/<int:quiz_id>/attempt/<int:attempt_id>/results/', attempt_detail, name='attempt-detail'),
]
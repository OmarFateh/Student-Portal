from django.urls import path

from .views import add_course_question, course_questions, question_detail, mark_as_answer, vote_answer

# namespace = question

urlpatterns = [
    path('courses/<slug:course_slug>/questions/', course_questions, name='course-questions'),
    path('courses/<slug:course_slug>/questions/add/', add_course_question, name='add-course-question'),
    path('courses/<slug:course_slug>/question/<int:question_id>/', question_detail, name='question-detail'),
    path('courses/<slug:course_slug>/question/<int:question_id>/vote/', vote_answer, name='vote-answer'),
    path('courses/<slug:course_slug>/question/<int:question_id>/<int:answer_id>/mark/', mark_as_answer, name='mark-answer'),   
]
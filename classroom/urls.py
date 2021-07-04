from django.urls import path

from .views import (
    categories, 
    category_courses, 
    my_courses,
    add_course, 
    course_detail, 
    update_course, 
    delete_course,
    enroll_course,
    course_grades,
    student_grades,
    grade_submission,
)

# namespace = classroom

urlpatterns = [
    path('courses/categories/', categories, name='categories'),
    path('courses/categories/<slug:category_slug>/', category_courses, name='category-courses'),
    path('my-courses/teaching/', my_courses, name='my-courses'),
    path('courses/add/', add_course, name='add-course'),
    path('courses/<slug:course_slug>/', course_detail, name='course-detail'),
    path('courses/<slug:course_slug>/update/', update_course, name='update-course'),
    path('courses/<slug:course_slug>/delete/', delete_course, name='delete-course'),
    path('courses/<slug:course_slug>/enroll/', enroll_course, name='enroll-course'),
    path('courses/<slug:course_slug>/grades/', course_grades, name='course-grades'),
    path('courses/<slug:course_slug>/student/grades/', student_grades, name='student-grades'),
    path('courses/<slug:course_slug>/submissions/<int:grade_id>/grade/', grade_submission, name='grade-submission'),

]
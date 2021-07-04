from django.urls import path

from .views import add_assignment, assignment_detail, submit_assignment

# namespace = assignment

urlpatterns = [
    path('courses/<slug:course_slug>/assignment/<int:assignment_id>/', assignment_detail, name='assignment-detail'),
    # Teacher
    path('courses/<slug:course_slug>/<int:module_id>/assignment/add/', add_assignment, name='add-assignment'),
    # Student
    path('courses/<slug:course_slug>/assignment/<int:assignment_id>/submit/', submit_assignment, name='submit-assignment'),
]
from django.urls import path

from .views import course_modules, add_module

# namespace = module

urlpatterns = [
    path('courses/<slug:course_slug>/modules/', course_modules, name='course-modules'),
    path('courses/<slug:course_slug>/modules/add/', add_module, name='add-module'),
]
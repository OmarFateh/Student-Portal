from django.urls import path

from .views import add_page, page_detail, mark_page_as_done

# namespace = page

urlpatterns = [
    path('courses/<slug:course_slug>/<int:page_id>/', page_detail, name='page-detail'),
    path('courses/<slug:course_slug>/page/<int:page_id>/done/', mark_page_as_done, name='mark-as-done'),
    path('courses/<slug:course_slug>/<int:module_id>/pages/add/', add_page, name='add-page'),
]
from django.urls import path
from .views import home_view, delete_event, save_event

urlpatterns = [
    path('', home_view, name='home_page'),
    path('delete-event/', delete_event, name='timetable-delete'),
    path('save-event/', save_event, name='timetable-save'),
]

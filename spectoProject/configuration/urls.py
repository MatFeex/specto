from django.urls import path
from . import views



urlpatterns = [
    path('',views.home, name="home"),
    # urls for DIVISION
    path('configuration/division/',views.read_division, name="division"),
    path('configuration/division/create-division/',views.create_division, name="create-division"),
    path('configuration/division/<id>/update-division/',views.update_division, name="update-division"),
    path('configuration/division/<id>/delete-division/',views.delete_division, name="delete-division"),
    path('configuration/division/<id>/restore-division/',views.restore_division, name="restore-division"),
]

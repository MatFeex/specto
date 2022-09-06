from django.urls import path
from . import views



urlpatterns = [
    path('',views.home, name="home"),
    
    # urls for DIVISION
    path('configuration/deleted-division/',views.read_deleted_division, name="deleted-division"),
    path('configuration/division/',views.read_division, name="division"),
    path('configuration/division/create-division/',views.create_division, name="create-division"),
    path('configuration/division/<division_id>/update-division/',views.update_division, name="update-division"),
    path('configuration/division/<division_id>/delete-division/',views.delete_division, name="delete-division"),
    path('configuration/division/<division_id>/restore-division/',views.restore_division, name="restore-division"),
    
    
    # urls for PROGRAM
    path('configuration/division/<division_id>/deleted-program/',views.read_deleted_program, name="deleted-program"),
    path('configuration/division/<division_id>/program/',views.read_program, name="program"),
    path('configuration/division/<division_id>/program/create-program/',views.create_program, name="create-program"),
    path('configuration/division/<division_id>/program/<program_id>/update-program/',views.update_program, name="update-program"),
    path('configuration/division/<division_id>/program/<program_id>/delete-program/',views.delete_program, name="delete-program"),
    path('configuration/division/<division_id>/program/<program_id>/restore-program/',views.restore_program, name="restore-program"),
]

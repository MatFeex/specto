from django.urls import path
from . import views


urlpatterns = [
    
    # urls for PASSATION
    path('passation/deleted-passation/',views.read_deleted_passation, name="deleted-passation"),
    path('passation/',views.read_passation, name="passation"),
    path('passation/create-passation/',views.create_passation, name="create-passation"),
    path('passation/<passation_id>/update-passation/',views.update_passation, name="update-passation"),
    path('passation/<passation_id>/delete-passation/',views.delete_passation, name="delete-passation"),
    path('passation/<passation_id>/restore-passation/',views.restore_passation, name="restore-passation"),
    path('passation/<passation_id>/passation-details/',views.read_specific_passation, name="passation-details"),
]

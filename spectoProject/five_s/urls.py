from django.urls import path
from . import views


urlpatterns = [
    
    # urls for CRITERIA
    path('configuration/criteria/deleted-criteria/',views.read_deleted_criteria, name="deleted-criteria"),
    path('configuration/criteria/',views.read_criteria, name="criteria"),
    path('configuration/criteria/create-criteria/',views.create_criteria, name="create-criteria"),
    path('configuration/criteria/<criteria_id>/update-criteria/',views.update_criteria, name="update-criteria"),
    path('configuration/criteria/<criteria_id>/delete-criteria/',views.delete_criteria, name="delete-criteria"),
    path('configuration/criteria/<criteria_id>/restore-criteria/',views.restore_criteria, name="restore-criteria"),

    # urls for 5S
    path('five-s/deleted-five-s/',views.read_deleted_five_s, name="deleted-five-s"),
    path('five-s/',views.read_five_s, name="five-s"),
    path('five-s/<five_s_id>/details/',views.read_specific_five_s, name="five-s-details"),
    path('five-s/create-five-s/',views.create_five_s, name="create-five-s"),
    path('five-s/<five_s_id>/update-five-s/',views.update_five_s, name="update-five-s"),
    path('five-s/<five_s_id>/delete-five-s/',views.delete_five_s, name="delete-five-s"),
    path('five-s/<five_s_id>/restore-five-s/',views.restore_five_s, name="restore-five-s"),
]

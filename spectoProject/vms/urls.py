from django.urls import path
from . import views


urlpatterns = [
    
    # urls for VMQ
    path('vms/deleted-vms/',views.read_deleted_vms, name="deleted-vms"),
    path('vms/',views.read_vms, name="vms"),
    path('vms/create-vms/',views.create_vms, name="create-vms"),
    # path('vms/vms-actions/',views.read_vms_actions, name="vms-actions"),
    path('vms/<vms_id>/update-vms/',views.update_vms, name="update-vms"),
    path('vms/<vms_id>/delete-vms/',views.delete_vms, name="delete-vms"),
    path('vms/<vms_id>/restore-vms/',views.restore_vms, name="restore-vms"),
    path('vms/<vms_id>/vms-details/',views.read_specific_vms, name="vms-details"),
]

from django.urls import path
from . import views


urlpatterns = [
    
    # urls for GEMBA SERVICE
    path('gemba/deleted-gemba-service/',views.read_deleted_gemba_service, name="deleted-gemba-service"),
    path('gemba/gemba-service/',views.read_gemba_service, name="gemba-service"),
    path('gemba/gemba-service/create-gemba-service/',views.create_gemba_service, name="create-gemba-service"),
    path('gemba/gemba-service/<gemba_service_id>/update-gemba-service/',views.update_gemba_service, name="update-gemba-service"),
    path('gemba/gemba-service/<gemba_service_id>/delete-gemba-service/',views.delete_gemba_service, name="delete-gemba-service"),
    path('gemba/gemba-service/<gemba_service_id>/restore-gemba-service/',views.restore_gemba_service, name="restore-gemba-service"),
    
    # urls for GEMBA ITEM
    path('gemba/gemba-service/<gemba_service_id>/deleted-gemba-gemba-item/',views.read_deleted_gemba_item, name="deleted-gemba-item"),
    path('gemba/gemba-service/<gemba_service_id>/gemba-item/',views.read_gemba_item, name="gemba-item"),
    path('gemba/gemba-service/<gemba_service_id>/gemba-item/create-gemba-item/',views.create_gemba_item, name="create-gemba-item"),
    path('gemba/gemba-service/<gemba_service_id>/gemba-item/<gemba_item_id>/update-gemba-item/',views.update_gemba_item, name="update-gemba-item"),
    path('gemba/gemba-service/<gemba_service_id>/gemba-item/<gemba_item_id>/delete-gemba-item/',views.delete_gemba_item, name="delete-gemba-item"),
    path('gemba/gemba-service/<gemba_service_id>/gemba-item/<gemba_item_id>/restore-gemba-item/',views.restore_gemba_item, name="restore-gemba-item"),
    
    # urls for GEMBA
    path('gemba/deleted-gemba/',views.read_deleted_gemba, name="deleted-gemba"),
    path('gemba/',views.read_gemba, name="gemba"),
    path('gemba/create-gemba/',views.create_gemba, name="create-gemba"),
    path('gemba/<gemba_id>/update-gemba/',views.update_gemba, name="update-gemba"),
    path('gemba/<gemba_id>/delete-gemba/',views.delete_gemba, name="delete-gemba"),
    path('gemba/<gemba_id>/restore-gemba/',views.restore_gemba, name="restore-gemba"),
    path('gemba/<gemba_id>/gemba-details/',views.read_specific_gemba, name="gemba-details"),
]

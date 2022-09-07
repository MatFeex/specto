from django.urls import path
from . import views


urlpatterns = [
    
    # urls for THEME
    path('vmq/deleted-theme/',views.read_deleted_theme, name="deleted-theme"),
    path('vmq/theme/',views.read_theme, name="theme"),
    path('vmq/theme/create-theme/',views.create_theme, name="create-theme"),
    path('vmq/theme/<theme_id>/update-theme/',views.update_theme, name="update-theme"),
    path('vmq/theme/<theme_id>/delete-theme/',views.delete_theme, name="delete-theme"),
    path('vmq/theme/<theme_id>/restore-theme/',views.restore_theme, name="restore-theme"),
    
    # urls for ITEM
    path('vmq/theme/<theme_id>/deleted-item/',views.read_deleted_item, name="deleted-item"),
    path('vmq/theme/<theme_id>/item/',views.read_item, name="item"),
    path('vmq/theme/<theme_id>/item/create-item/',views.create_item, name="create-item"),
    path('vmq/theme/<theme_id>/item/<item_id>/update-item/',views.update_item, name="update-item"),
    path('vmq/theme/<theme_id>/item/<item_id>/delete-item/',views.delete_item, name="delete-item"),
    path('vmq/theme/<theme_id>/item/<item_id>/restore-item/',views.restore_item, name="restore-item"),
]

from django.urls import path
from . import views


urlpatterns = [
    
    # urls for QUALITY REFERENCE
    path('vmq/quality_reference/deleted-quality_reference/',views.read_deleted_quality_reference, name="deleted-quality-reference"),
    path('vmq/quality_reference/',views.read_quality_reference, name="quality-reference"),
    path('vmq/quality_reference/create-quality_reference/',views.create_quality_reference, name="create-quality-reference"),
    path('vmq/quality_reference/<quality_reference_id>/update-quality_reference/',views.update_quality_reference, name="update-quality-reference"),
    path('vmq/quality_reference/<quality_reference_id>/delete-quality_reference/',views.delete_quality_reference, name="delete-quality-reference"),
    path('vmq/quality_reference/<quality_reference_id>/restore-quality_reference/',views.restore_quality_reference, name="restore-quality-reference"),

    # urls for THEME
    path('vmq/quality_reference/<quality_reference_id>/theme/deleted-theme/',views.read_deleted_theme, name="deleted-theme"),
    path('vmq/quality_reference/<quality_reference_id>/theme/',views.read_theme, name="theme"),
    path('vmq/quality_reference/<quality_reference_id>/theme/create-theme/',views.create_theme, name="create-theme"),
    path('vmq/quality_reference/<quality_reference_id>/theme/<theme_id>/update-theme/',views.update_theme, name="update-theme"),
    path('vmq/quality_reference/<quality_reference_id>/theme/<theme_id>/delete-theme/',views.delete_theme, name="delete-theme"),
    path('vmq/quality_reference/<quality_reference_id>/theme/<theme_id>/restore-theme/',views.restore_theme, name="restore-theme"),
    
    # urls for ITEM
    path('vmq/quality_reference/<quality_reference_id>/theme/<theme_id>/item/deleted-item/',views.read_deleted_item, name="deleted-item"),
    path('vmq/quality_reference/<quality_reference_id>/theme/<theme_id>/item/',views.read_item, name="item"),
    path('vmq/quality_reference/<quality_reference_id>/theme/<theme_id>/item/create-item/',views.create_item, name="create-item"),
    path('vmq/quality_reference/<quality_reference_id>/theme/<theme_id>/item/<item_id>/update-item/',views.update_item, name="update-item"),
    path('vmq/quality_reference/<quality_reference_id>/theme/<theme_id>/item/<item_id>/delete-item/',views.delete_item, name="delete-item"),
    path('vmq/quality_reference/<quality_reference_id>/theme/<theme_id>/item/<item_id>/restore-item/',views.restore_item, name="restore-item"),
    
    # urls for VMQ
    path('vmq/deleted-vmq/',views.read_deleted_vmq, name="deleted-vmq"),
    path('vmq/',views.read_vmq, name="vmq"),
    path('vmq/create-vmq/',views.create_vmq, name="create-vmq"),
    path('vmq/vmq-actions/',views.read_vmq_actions, name="vmq-actions"),
    path('vmq/<vmq_id>/update-vmq/',views.update_vmq, name="update-vmq"),
    path('vmq/<vmq_id>/delete-vmq/',views.delete_vmq, name="delete-vmq"),
    path('vmq/<vmq_id>/restore-vmq/',views.restore_vmq, name="restore-vmq"),
    path('vmq/<vmq_id>/vmq-details/',views.read_specific_vmq, name="vmq-details"),

    # urls for VMQ - KPI
    path('vmq-kpi/',views.vmq_kpi, name="vmq-kpi"),
    path('vmq-kpi/select-range',views.select_range, name="vmq-kpi-select-range"),
]

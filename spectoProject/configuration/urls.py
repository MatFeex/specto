from django.urls import path
from . import views


urlpatterns = [
    
    # url for HOME
    path('',views.home, name="home"),
    
    # urls for DIVISION
    path('configuration/division/deleted-division/',views.read_deleted_division, name="deleted-division"),
    path('configuration/division/',views.read_division, name="division"),
    path('configuration/division/create-division/',views.create_division, name="create-division"),
    path('configuration/division/<division_id>/update-division/',views.update_division, name="update-division"),
    path('configuration/division/<division_id>/delete-division/',views.delete_division, name="delete-division"),
    path('configuration/division/<division_id>/restore-division/',views.restore_division, name="restore-division"),
    
    # urls for PROGRAM
    path('configuration/division/<division_id>/program/deleted-program/',views.read_deleted_program, name="deleted-program"),
    path('configuration/division/<division_id>/program/',views.read_program, name="program"),
    path('configuration/division/<division_id>/program/create-program/',views.create_program, name="create-program"),
    path('configuration/division/<division_id>/program/<program_id>/update-program/',views.update_program, name="update-program"),
    path('configuration/division/<division_id>/program/<program_id>/delete-program/',views.delete_program, name="delete-program"),
    path('configuration/division/<division_id>/program/<program_id>/restore-program/',views.restore_program, name="restore-program"),

    # urls for PRODUCT
    path('configuration/division/<division_id>/program/<program_id>/product/deleted-product/',views.read_deleted_product, name="deleted-product"),
    path('configuration/division/<division_id>/program/<program_id>/product/',views.read_product, name="product"),
    path('configuration/division/<division_id>/program/<program_id>/product/create-product/',views.create_product, name="create-product"),
    path('configuration/division/<division_id>/program/<program_id>/product/<product_id>/update-product/',views.update_product, name="update-product"),
    path('configuration/division/<division_id>/program/<program_id>/product/<product_id>/delete-product/',views.delete_product, name="delete-product"),
    path('configuration/division/<division_id>/program/<program_id>/product/<product_id>/restore-product/',views.restore_product, name="restore-product"),

    # urls for WORKSHOP
    path('configuration/division/<division_id>/program/<program_id>/product/<product_id>/workshop/deleted-workshop/',views.read_deleted_workshop, name="deleted-workshop"),
    path('configuration/division/<division_id>/program/<program_id>/product/<product_id>/workshop/',views.read_workshop, name="workshop"),
    path('configuration/division/<division_id>/program/<program_id>/product/<product_id>/workshop/create-workshop/',views.create_workshop, name="create-workshop"),
    path('configuration/division/<division_id>/program/<program_id>/product/<product_id>/workshop/<workshop_id>/update-workshop/',views.update_workshop, name="update-workshop"),
    path('configuration/division/<division_id>/program/<program_id>/product/<product_id>/workshop/<workshop_id>/delete-workshop/',views.delete_workshop, name="delete-workshop"),
    path('configuration/division/<division_id>/program/<program_id>/product/<product_id>/workshop/<workshop_id>/restore-workshop/',views.restore_workshop, name="restore-workshop"),

    # urls for QUALIFICATIONS
    path('configuration/qualification/deleted-qualification/',views.read_deleted_qualification, name="deleted-qualification"),
    path('configuration/qualification/',views.read_qualification, name="qualification"),
    path('configuration/qualification/create-qualification/',views.create_qualification, name="create-qualification"),
    path('configuration/qualification/<qualification_id>/update-qualification/',views.update_qualification, name="update-qualification"),
    path('configuration/qualification/<qualification_id>/delete-qualification/',views.delete_qualification, name="delete-qualification"),
    path('configuration/qualification/<qualification_id>/restore-qualification/',views.restore_qualification, name="restore-qualification"),

    # urls VMS PLANNING
    path('configuration/planning/vms-planning/planning/',views.vms_planning, name="vms-planning"),
    path('configuration/planning/vms-planning/create-planning/',views.create_vms_planning, name="create-vms-planning"),

    # urls VMQ PLANNING
    path('configuration/planning/vmq-planning/planning-list/',views.vmq_planning_list, name="vmq-planning-list"),
    path('configuration/planning/vmq-planning/<str:month>/<str:year>/planning/',views.vmq_planning, name="vmq-planning"),
    path('configuration/planning/vmq-planning/create-planning/',views.create_vmq_planning, name="create-vmq-planning"),
    path('configuration/planning/vmq-planning/planning/<str:month>/<str:year>/create-row-vmq-planning/',views.create_row_vmq_planning, name="create-row-vmq-planning"),

    # urls for EMPLOYEE
    path('configuration/employee/',views.read_employee, name="employee"),
    path('configuration/employee/upload-employee/',views.upload_employee, name="upload-employee"),
]

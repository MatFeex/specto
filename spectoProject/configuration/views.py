from django.shortcuts import render, redirect
from .models import Division, Employee, Program, Product, VMS_Planning, Workshop, Qualification, VMQ_Planning
from vms.models import Vms

from .forms import DivisionForm, EmployeeFileForm, EmployeeForm, ProgramForm, ProductForm, VMQ_PlanningForm, WorkshopForm, QualificationForm, VMS_PlanningForm, VMQ_PlanningForm_Custom
from django.contrib import messages
from django.db.models import Q

import os
import pandas as pd
from itertools import cycle
import math

# SPECTO VIEWS - CONFIGURATION :

def home(request):
    return render(request,'configuration/home.html')


# CRUD-R for DIVISION
def read_division(request):
    divisions = Division.objects.all()
    division_count = divisions.count()
    context = {'divisions':divisions,'division_count':division_count}
    return render(request,'configuration/division/division.html',context)


def read_deleted_division(request):
    divisions = Division.deleted_objects.all()
    division_count = divisions.count()
    context = {'divisions':divisions,'division_count':division_count}
    return render(request,'configuration/division/deleted_division.html',context)


def create_division(request):
    form = DivisionForm()
    if request.method == 'POST' :
        form = DivisionForm(request.POST)
        if form.is_valid(): 
            form.save()
            return redirect('division')
        else : messages.error(request, 'An error occurred while adding a division')
    context = {'form':form, 'text':'CREATE A NEW DIVISION'}
    return render(request, 'configuration/form.html', context)


def update_division(request,division_id):
    division = Division.objects.get(id=division_id)
    form = DivisionForm(instance=division)
    if request.method == 'POST' :
        form = DivisionForm(request.POST, instance=division)
        if form.is_valid() : 
            form.save()
            return redirect('division')
        else : messages.error(request, 'An error occurred while updating the division')
    context = {'form':form,'text':'UPDATE THE DIVISION'}
    return render(request, 'configuration/form.html', context)


def delete_division(request,division_id):
    division = Division.objects.get(id=division_id)
    if request.method == 'POST' :
        division.soft_deleted()
        return redirect('division')
    context = {'obj':division}
    return render(request,'configuration/delete.html',context)


def restore_division(request,division_id):
    division = Division.deleted_objects.get(id=division_id)
    if request.method == 'POST' :
        division.restore()
        return redirect('division')

    context = {'obj':division}
    return render(request,'configuration/restore.html',context)


# CRUD-R for PROGRAM

def read_program(request, division_id):
    programs = Program.objects.filter(division_id=division_id)
    program_count = programs.count()
    context = {'programs':programs,'program_count':program_count,'division_id':division_id}
    return render(request,'configuration/program/program.html',context)


def read_deleted_program(request, division_id):
    programs = Program.deleted_objects.filter(division_id=division_id)
    program_count = programs.count()
    context = {'programs':programs,'program_count':program_count,'division_id':division_id}
    return render(request,'configuration/program/deleted_program.html',context)


def create_program(request, division_id):
    form = ProgramForm()
    if request.method == 'POST' :
        form = ProgramForm(request.POST)
        if form.is_valid(): 
            form.division_id = division_id
            f = form.save(commit=False)
            f.division_id = division_id
            f.save()
            return redirect(f'/configuration/division/{division_id}/program/')
        else : messages.error(request, 'An error occurred while adding the program')
    context = {'form':form, 'text':'CREATE A NEW PROGRAM'}
    return render(request, 'configuration/form.html', context)


def update_program(request,division_id, program_id):
    program = Program.objects.get(id=program_id)
    form = ProgramForm(instance=program)
    if request.method == 'POST' :
        form = ProgramForm(request.POST, instance=program)
        if form.is_valid() : 
            form.division_id = division_id
            f = form.save(commit=False)
            f.division_id = division_id
            f.save()
            return redirect(f'/configuration/division/{division_id}/program/')
        else : messages.error(request, 'An error occurred while updating the program')
    context = {'form':form, 'text':'UPDATE THE PROGRAM'}
    return render(request, 'configuration/form.html', context)


def delete_program(request,division_id, program_id):
    program = Program.objects.get(id=program_id)
    if request.method == 'POST' :
        program.soft_deleted()
        return redirect(f'/configuration/division/{division_id}/program/')
    context = {'obj':program}
    return render(request,'configuration/delete.html',context)


def restore_program(request,division_id, program_id):
    program = Program.deleted_objects.get(id=program_id)
    if request.method == 'POST' :
        program.restore()
        return redirect(f'/configuration/division/{division_id}/program/')

    context = {'obj':program}
    return render(request,'configuration/restore.html',context)


# CRUD-R for PRODUCT

def read_product(request, division_id, program_id):
    products = Product.objects.filter(program_id=program_id)
    product_count = products.count()
    context = {'products':products,'product_count':product_count,'division_id':division_id, 'program_id':program_id}
    return render(request,'configuration/product/product.html',context)


def read_deleted_product(request, division_id, program_id):
    products = Product.deleted_objects.filter(program_id=program_id)
    product_count = products.count()
    context = {'products':products,'product_count':product_count,'division_id':division_id,'program_id':program_id}
    return render(request,'configuration/product/deleted_product.html',context)


def create_product(request, division_id, program_id):
    form = ProductForm()
    if request.method == 'POST' :
        form = ProductForm(request.POST)
        if form.is_valid(): 
            form.program_id = program_id
            f = form.save(commit=False)
            f.program_id = program_id
            f.save()
            return redirect(f'/configuration/division/{division_id}/program/{program_id}/product/')
        else : messages.error(request, 'An error occurred while adding the product')
    context = {'form':form, 'text':'CREATE A NEW PRODUCT'}
    return render(request, 'configuration/form.html', context)


def update_product(request,division_id, program_id, product_id):
    product = Product.objects.get(id=product_id)

    form = ProductForm(instance=product)
    if request.method == 'POST' :
        form = ProgramForm(request.POST, instance=product)
        if form.is_valid() : 
            form.program_id = program_id
            f = form.save(commit=False)
            f.program_id = program_id
            f.save()
            return redirect(f'/configuration/division/{division_id}/program/{program_id}/product/')
        else : messages.error(request, 'An error occurred while updating the product')
    context = {'form':form,'text':'UPDATE THE PRODUCT'}
    return render(request, 'configuration/form.html', context)


def delete_product(request,division_id, program_id, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST' :
        product.soft_deleted()
        return redirect(f'/configuration/division/{division_id}/program/{program_id}/product/')
    context = {'obj':product}
    return render(request,'configuration/delete.html',context)


def restore_product(request,division_id, program_id, product_id):
    product = Product.deleted_objects.get(id=product_id)
    if request.method == 'POST' :
        product.restore()
        return redirect(f'/configuration/division/{division_id}/program/{program_id}/product/')

    context = {'obj':product}
    return render(request,'configuration/restore.html',context)


# CRUD-R for WORKSHOP

def read_workshop(request, division_id, program_id, product_id):
    workshops = Workshop.objects.filter(product_id=product_id)
    workshop_count = workshops.count()
    context = {'workshops':workshops,'workshop_count':workshop_count,'division_id':division_id, 'program_id':program_id, 'product_id':product_id}
    return render(request,'configuration/workshop/workshop.html',context)


def read_deleted_workshop(request, division_id, program_id, product_id):
    workshops = Workshop.deleted_objects.filter(product_id=product_id)
    workshop_count = workshops.count()
    context = {'workshops':workshops,'workshop_count':workshop_count,'division_id':division_id, 'program_id':program_id, 'product_id':product_id}
    return render(request,'configuration/workshop/deleted_workshop.html',context)


def create_workshop(request, division_id, program_id, product_id):
    form = WorkshopForm()
    if request.method == 'POST' :
        form = WorkshopForm(request.POST)
        if form.is_valid(): 
            form.product_id = product_id
            f = form.save(commit=False)
            f.product_id = product_id
            f.save()
            return redirect(f'/configuration/division/{division_id}/program/{program_id}/product/{product_id}/workshop/')
        else : messages.error(request, 'An error occurred while adding the workshop')
    context = {'form':form, 'text':'CREATE A NEW WORKSHOP'}
    return render(request, 'configuration/form.html', context)


def update_workshop(request,division_id, program_id, product_id, workshop_id):
    workshop = Workshop.objects.get(id=workshop_id)
    form = WorkshopForm(instance=workshop)
    if request.method == 'POST' :
        form = WorkshopForm(request.POST, instance=workshop)
        if form.is_valid() : 
            form.product_id = product_id
            f = form.save(commit=False)
            f.product_id = product_id
            f.save()
            return redirect(f'/configuration/division/{division_id}/program/{program_id}/product/{product_id}/workshop/')
        else : messages.error(request, 'An error occurred while updating the workshop')
    context = {'form':form, 'text':'UPDATE THE WORKSHOP'}
    return render(request, 'configuration/form.html', context)


def delete_workshop(request,division_id, program_id, product_id, workshop_id):
    workshop = Workshop.objects.get(id=workshop_id)
    if request.method == 'POST' :
        workshop.soft_deleted()
        return redirect(f'/configuration/division/{division_id}/program/{program_id}/product/{product_id}/workshop/')
    context = {'obj':workshop}
    return render(request,'configuration/delete.html',context)


def restore_workshop(request,division_id, program_id, product_id, workshop_id):
    workshop = Workshop.deleted_objects.get(id=workshop_id)
    if request.method == 'POST' :
        workshop.restore()
        return redirect(f'/configuration/division/{division_id}/program/{program_id}/product/{product_id}/workshop/')
    context = {'obj':workshop}
    return render(request,'configuration/restore.html',context)


# « CRUD-R » for EMPLOYEE

def read_employee(request):
    employees = Employee.objects.all()
    employee_count = employees.count()
    context = {'employees':employees,'employee_count':employee_count}
    return render(request,'configuration/employee/employee.html',context)

def upload_employee(request):

    # UPLOAD THE EMPLOYEE DATA FILE
    form = EmployeeFileForm()

    if request.method == 'POST':
        form = EmployeeFileForm(request.POST, request.FILES) 
        if form.is_valid(): 
            # DELETE PREVIOUS UPLOADED FILE
            for file in os.listdir("configuration/handle_uploaded_file") : os.remove(f'configuration/handle_uploaded_file/{file}')
            # keep an uploaded files history in EmployeeFile Model
            form.save() 
            # PATH OF NEW UPLOADED FILE 
            file_path = os.getcwd().replace("\\",'/') + '/configuration/handle_uploaded_file/' + os.listdir("configuration/handle_uploaded_file")[0]

            if os.path.isfile(file_path) : 
                #try: 


                # DATA PROCESSING
                data = pd.read_excel(file_path) # read the new uploaded file
                
                # get objects
                programs = Program.objects.values('name','id')
                products = Product.objects.values('name','id')
                workshops = Workshop.objects.values('name','id')
                # obj to df
                df_programs = pd.DataFrame(list(programs))
                df_products = pd.DataFrame(list(products))
                df_workshop = pd.DataFrame(list(workshops))
                
                # df to dict
                dict_programs, dict_products, dict_workshop = [],[],[]
                try :
                    dict_programs = dict(zip(df_programs.name,df_programs.id))
                    dict_products = dict(zip(df_products.name,df_products.id))
                    dict_workshop = dict(zip(df_workshop.name,df_workshop.id))
                except : messages.error(request, 'Default values will be given for missing information about programs, products and workshops')
                
                # mapping
                program_id = data['Affaire'].map(dict_programs)
                product_id = data['Produit'].map(dict_products)
                workshop_id = data['Phase'].map(dict_workshop)

                # give default ID if cannot map
                program_id = [Program.objects.filter(name='NA').first().id if math.isnan(float(idd)) else idd for idd in program_id]
                product_id = [Product.objects.filter(name='NA').first().id if math.isnan(float(idd)) else idd for idd in product_id]
                workshop_id = [Workshop.objects.filter(name='NA').first().id if math.isnan(float(idd)) else idd for idd in workshop_id]

                # delete useless columns
                data = data.drop(columns=['Affaire', 'Produit','Phase'])

                data.insert(13,'division_id',1) # add DIVISION column that doesn't exist in the file
                data.insert(14,'program_id',program_id)
                data.insert(15,'product_id',product_id)
                data.insert(16,'workshop_id',workshop_id)

                for i in range(len(data)):
                    matricule = data.loc[i,'Mat']
                    employee = Employee.objects.filter(matricule=matricule).first()
                    if employee : 
                        employee_form = EmployeeForm(instance=employee).save(commit=False)                
                        employee_form.matricule = data.iloc[i,0]
                        employee_form.names = data.iloc[i,1]
                        employee_form.i_p = data.iloc[i,2]
                        employee_form.code = data.iloc[i,3]
                        employee_form.department = data.iloc[i,4]
                        employee_form.wording = data.iloc[i,5]
                        employee_form.cost_center = data.iloc[i,6]
                        employee_form.job_bulletin = data.iloc[i,7]
                        employee_form.resp_matricule_n1 = data.iloc[i,8]
                        employee_form.resp_names_n1 = data.iloc[i,9]
                        employee_form.resp_matricule_n2 = data.iloc[i,10]
                        employee_form.resp_names_n2 = data.iloc[i,11]
                        employee_form.staff_tab_afs = data.iloc[i,12]
                        employee_form.division_id = data.iloc[i,13]
                        employee_form.program_id = data.iloc[i,14]
                        employee_form.product_id = data.iloc[i,15]
                        employee_form.workshop_id = data.iloc[i,16]
                        employee_form.save()
                    else:
                        Employee.objects.create(
                            matricule = data.iloc[i,0],
                            names = data.iloc[i,1],
                            i_p = data.iloc[i,2],
                            code = data.iloc[i,3],
                            department = data.iloc[i,4],
                            wording = data.iloc[i,5],
                            cost_center = data.iloc[i,6],
                            job_bulletin = data.iloc[i,7],
                            resp_matricule_n1 = data.iloc[i,8],
                            resp_names_n1 = data.iloc[i,9],
                            resp_matricule_n2 = data.iloc[i,10],
                            resp_names_n2 = data.iloc[i,11],
                            staff_tab_afs = data.iloc[i,12],
                            division_id = data.iloc[i,13],
                            program_id = data.iloc[i,14],
                            product_id = data.iloc[i,15],
                            workshop_id = data.iloc[i,16],
                        )
                return redirect('employee')

                #except : messages.error(request, 'File not valid : it must contain at least 16 columns.')
            
            else : messages.error(request, 'The path file is unreachable')

        else : messages.error(request, 'An error occurred : file not valid')

    context = {'form':form}
    return render(request,'configuration/employee/upload_employee.html',context)



# # CONNETION TO DATABASE
# conn = psycopg2.connect(host='localhost',dbname='specto_db',user='postgres',password='specto777',port='5432')

# empoyee_file = StringIO()
# empoyee_file.write(data.to_csv(index=None, header=None,sep=';'))
# empoyee_file.seek(0)
# with conn.cursor() as c:
#     c.copy_from(
#         file=empoyee_file,
#         null="",
#         sep=";",
#         table='configuration_employee',
#         columns=[
#             'matricule',
#             'names',
#             'i_p',
#             'code', 
#             'department',
#             'wording',
#             'cost_center',
#             'job_bulletin',
#             'resp_matricule_n1',
#             'resp_names_n1',
#             'resp_matricule_n2',
#             'resp_names_n2',
#             'staff_tab_afs',
#             'division_id',
#             'program_id',
#             'product_id',
#             'workshop_id',
#         ]
#     )
# try :
#     conn.commit()
#     return redirect('employee')
# except : messages.error(request, 'An error occured : please register at least a divison, a program, a product and a workshop before uploading employees')


# CRUD-R for DIVISION
def read_qualification(request):
    qualifications = Qualification.objects.all()
    qualification_count = qualifications.count()
    context = {'qualifications':qualifications,'qualification_count':qualification_count}
    return render(request,'configuration/qualification/qualification.html',context)


def read_deleted_qualification(request):
    qualifications = Qualification.deleted_objects.all()
    qualification_count = qualifications.count()
    context = {'qualifications':qualifications,'qualification_count':qualification_count}
    return render(request,'configuration/qualification/deleted_qualification.html',context)


def create_qualification(request):
    form = QualificationForm()
    if request.method == 'POST' :
        employee_id = request.POST.get('employee')
        qualification = Qualification.objects.filter(employee_id=employee_id).first()
        if qualification : 
            update_qualification(request,qualification.id)
            return redirect('qualification')
        else :
            form = QualificationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('qualification')
            else : messages.error(request, 'An error occurred while adding a qualification')
    context = {'form':form, 'text':'CREATE A NEW QUALIFICATION'}
    return render(request, 'configuration/form.html', context)


def update_qualification(request,qualification_id):
    qualification = Qualification.objects.get(id=qualification_id)
    form = QualificationForm(instance=qualification)
    if request.method == 'POST' :
        form = QualificationForm(request.POST, instance=qualification)
        if form.is_valid() : 
            form.save()
            return redirect('qualification')
        else : messages.error(request, 'An error occurred while updating the qualification')
    context = {'form':form,'text':'UPDATE THE QUALIFICATION'}
    return render(request, 'configuration/form.html', context)


def delete_qualification(request,qualification_id):
    qualification = Qualification.objects.get(id=qualification_id)
    if request.method == 'POST' :
        qualification.soft_deleted()
        return redirect('qualification')
    context = {'obj':qualification}
    return render(request,'configuration/delete.html',context)


def restore_qualification(request,qualification_id):
    qualification = Qualification.deleted_objects.get(id=qualification_id)
    if request.method == 'POST' :
        qualification.restore()
        return redirect('qualification')

    context = {'obj':qualification}
    return render(request,'configuration/restore.html',context)


# VMS PLANNING

def vms_planning(request):
    vms_planning = VMS_Planning.objects.all().order_by('-year')
    return render(request,'configuration/planning/vms/vms_planning.html',{'vms_planning':vms_planning})


def create_vms_planning(request):


    if request.method == 'POST':

        # GET PLANNING DATES
        month = request.POST.get('month')
        year = request.POST.get('year')

        # delete previous planning one the same period
        VMS_Planning.objects.filter(month=month,year=year).delete()

        # GET employees QUALIFIED
        employees_qualified = Qualification.objects.filter(vms_qualification=True).values_list('employee', flat=True)
        count_qualified = employees_qualified.count()
        
        # GET employees already VISITED
        vms_employee_visited = VMS_Planning.objects.filter(closed=True).values_list('vms_employee_visited', flat=True)

        # # GET employees NOT VISITED
        employee_not_visited = Employee.objects.exclude(matricule__in=vms_employee_visited).values_list('matricule', flat=True)
        count_not_visited = employee_not_visited.count()

        # if NB Employees To Visit >= NB Employees Qualified * 2 --> Next visited are only in Employee database
        if count_not_visited >= count_qualified*2 : 
            employee_to_be_visited = employee_not_visited[:count_qualified*2]
       
        else : # if NB Employees To Visit < NB Employees Qualified * 2 --> Next visited are the ones in Employee database + The first ones already visited
            employees = Employee.objects.values_list('matricule', flat=True) 
            employee_to_be_visited = employee_not_visited + employees
            employee_to_be_visited = employee_to_be_visited[:count_qualified*2]


        zip_list = dict( zip(employee_to_be_visited, cycle(employees_qualified)) if len(employee_to_be_visited) > len(employees_qualified) else zip(cycle(employee_to_be_visited), employees_qualified))

        # for vms_employee_qualified in employees_qualified : 
        for visited,user in zip_list.items() : 
            form = VMS_PlanningForm().save(commit=False)
            form.vms_vms_employee_qualified_id = user
            form.vms_vms_employee_visited_id = visited
            form.month = month
            form.year = year
            form.save()

        return redirect('vms-planning')
        
    return render(request,'configuration/planning/vms/vms_planning_date.html')


# VMQ PLANNING

def vmq_planning_list(request):
    vmq_plannings = []
    vmq_planning_all = VMQ_Planning.objects.all()
    months_years = list(set(vmq_planning_all.values_list('month','year')))
    for i in range(len(months_years)):
        vmq_plannings.append(vmq_planning_all.filter(month=months_years[i][0],year=months_years[i][1]))
    return render(request,'configuration/planning/vmq/vmq_planning_list.html',{'vmq_plannings':vmq_plannings})

def vmq_planning(request, month, year):
    vmq_planning = VMQ_Planning.objects.filter(month=month,year=year).order_by('-created_at',)
    if request.method == 'POST': 
        print(request.POST.get('row_to_remove'))
        VMQ_Planning.objects.filter(id = request.POST.get('row_to_remove')).delete()
        return render(request,'configuration/planning/vmq/vmq_planning.html',{'vmq_planning':vmq_planning})
    return render(request,'configuration/planning/vmq/vmq_planning.html',{'vmq_planning':vmq_planning})

def create_row_vmq_planning(request,month,year):
    if request.method == 'POST' :
        form = VMQ_PlanningForm_Custom(request.POST)
        if form.is_valid(): 
            form.month = month
            form.year = year
            f = form.save(commit=False)
            f.month = month
            f.year = year
            f.save()
            return redirect(f'/configuration/planning/vmq-planning/{month}/{year}/planning/')
        else : messages.error(request, 'An error occurred while adding the row in the specific VMQ Planning')
    else : form = VMQ_PlanningForm_Custom()
    context = {'form':form, 'text': f'VMQ PLANNING - add a row - {month} {year}'}
    return render(request, 'configuration/form.html', context)

def create_vmq_planning(request):

    if request.method == 'POST':

        # GET PLANNING DATES
        month = request.POST.get('month')
        year = request.POST.get('year')

        # delete previous planning one the same period
        VMQ_Planning.objects.filter(month=month,year=year).delete()

        # GET employees QUALIFIED - All

        qualified_employee = dict(list(Qualification.objects.filter(vmq_qualification=True).values_list('employee','employee__job_bulletin')))
        qualified_matricule = list(qualified_employee.keys())
        job_qualified = ["Responsable Fabrication","Chef d'équipe"]
        count_qualified = len(qualified_employee)

        # GET employees already VISITED
        visited_matricule = list(VMQ_Planning.objects.filter(closed=True).values_list('vmq_employee_visited', flat=True))

        # GET employees NOT VISITED
        job_visited = ['Manoeuvre spécialisé(e)','Contrôleur (se)']
        employee_not_visited = Employee.objects.filter(job_bulletin__in=job_visited).exclude(matricule__in=visited_matricule+qualified_matricule).values_list('matricule','resp_matricule_n1')
        count_not_visited = len(employee_not_visited)

        if count_not_visited >= count_qualified : 
            employee_not_visited = dict(list(employee_not_visited))
        else : 
            employees_loop = Employee.objects.values_list('matricule','resp_matricule_n1') # they become 'not visited'
            employee_not_visited = dict(list((employee_not_visited | employees_loop)))# [:delta]?

        for matricule,job in qualified_employee.items() :
            for matricule_to_visit,resp_n1 in employee_not_visited.items() :
                
                form = VMQ_PlanningForm().save(commit=False)
                form.month = month
                form.year = year
                if job in job_qualified:
                    if matricule == resp_n1 : 
                        form.vmq_employee_qualified_id = matricule  
                        form.vmq_employee_visited_id = matricule_to_visit
                        form.save()
                        del employee_not_visited[matricule_to_visit]
                        break
                else : 
                    form.vmq_employee_qualified_id = matricule
                    form.vmq_employee_visited_id = matricule_to_visit
                    form.save()
                    del employee_not_visited[matricule_to_visit]
                    break

        return redirect('vmq-planning-list')
        
    return render(request,'configuration/planning/vmq/vmq_planning_date.html')


# vmq_qualified = [
#     81371,
#     82206,
#     80197,
#     80608,
#     81301,
#     81996,
#     81951,
#     81997,
#     80111,
#     81360,
#     80124,
#     80319,
#     80363,
#     80378,
#     80421,
#     80640,
#     80687,
#     81144,
#     82063,
#     82309,
#     81200,
#     80062,
#     80968,
#     81846,
#     81851,
#     82162,
#     82307,
#     80036,
#     80706,
#     80289,
#     80655,
#     80040,
#     81934,
#     81201,
#     82061,
#     82275,
#     80143,
#     82058,
#     82065,
#     82164,
#     82264,
#     80109,
#     82213,
#     82166,
#     80688,
#     81486,
#     81802,
#     81835,
#     81932,
#     82163,
#     80807,
#     80352,
#     82204,
#     82205,
#     82322,
#     81179,
#     80906,
#     82305,
# ]
# for mat in vmq_qualified :
#     form = QualificationForm().save(commit=False)
#     form.employee_id = mat
#     form.vms_qualification = False
#     form.vmq_qualification = True
#     form.fives_qualification = False
#     form.save()
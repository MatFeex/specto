from itertools import product
from django.shortcuts import render, redirect
from .models import Division, Employee, Program, Product, Workshop, Qualification
from .forms import DivisionForm, EmployeeFileForm, ProgramForm, ProductForm, WorkshopForm, QualificationForm
from django.contrib import messages

import os
import psycopg2
import pandas as pd
from io import StringIO 


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
    print(workshop_id)
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

            # PATH OF NEW UPLOADED FILE 
            file_path = os.getcwd().replace("\\",'/') + '/configuration/handle_uploaded_file/' + os.listdir("configuration/handle_uploaded_file")[0]

            if os.path.isfile(file_path) : 

                # DELETE PREVIOUS UPLOADED FILE
                for file in os.listdir("configuration/handle_uploaded_file") : os.remove(f'configuration/handle_uploaded_file/{file}')
            
                form.save() # keep an uploaded files history in EmployeeFile Model

                # DELETE PREVIOUS EMPLOYEE DATA IN EMPLOYEE DATABASE
                Employee.objects.all().delete()

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
                program_id = data['Affaire'].map(dict_programs).values[0] if dict_programs else 'nan'
                product_id = data['Produit'].map(dict_products).values[0] if dict_products else 'nan'
                workshop_id = data['Phase'].map(dict_workshop).values[0] if dict_workshop else 'nan'

                # give default ID if cannot map
                program_id = int(str(program_id).replace('nan','1'))
                product_id = int(str(product_id).replace('nan','1'))
                workshop_id = int(str(workshop_id).replace('nan','1'))

                # delete useless columns
                data = data.drop(columns=['Affaire', 'Produit','Phase'])

                data.insert(13,'division_id',1) # add DIVISION column that doesn't exist in the file
                data.insert(14,'program_id',program_id)
                data.insert(15,'product_id',product_id)
                data.insert(16,'workshop_id',workshop_id)

                print(data)

                
                # CONNETION TO DATABASE
                conn = psycopg2.connect(host='localhost',dbname='specto_db',user='postgres',password='specto777',port='5432')

                empoyee_file = StringIO()
                empoyee_file.write(data.to_csv(index=None, header=None,sep=';'))
                empoyee_file.seek(0)
                with conn.cursor() as c:
                    c.copy_from(
                        file=empoyee_file,
                        null="",
                        sep=";",
                        table='configuration_employee',
                        columns=[
                            'matricule',
                            'names',
                            'i_p',
                            'code', 
                            'department',
                            'wording',
                            'cost_center',
                            'job_bulletin',
                            'resp_matricule_n1',
                            'resp_names_n1',
                            'resp_matricule_n2',
                            'resp_names_n2',
                            'staff_tab_afs',
                            'division_id',
                            'program_id',
                            'product_id',
                            'workshop_id',
                        ]
                    )
                try :
                    conn.commit()
                    return redirect('employee')
                except : messages.error(request, 'An error occured : please register at least a divison, a program, a product and a workshop before uploading employees')

            else : messages.error(request, 'The path file is unreachable')

        else : messages.error(request, 'An error occurred : file not valid')

    context = {'form':form}
    return render(request,'configuration/employee/upload_employee.html',context)


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
        form = QualificationForm(request.POST)
        if form.is_valid(): 
            form.save()
            return redirect('qualification')
        else : messages.error(request, 'An error occurred while adding a qualification')
    context = {'form':form, 'text':'CREATE A NEW DIVISION'}
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
    context = {'form':form,'text':'UPDATE THE DIVISION'}
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

from django.shortcuts import render, redirect
from .models import Division, Program, Product, Workshop
from .forms import DivisionForm, ProgramForm, ProductForm, WorkshopForm


# Create your views here.
def home(request):
    return render(request,'configuration/home.html')

# CRUD-R for DIVISION
def read_division(request):

    divisions = Division.objects.all()
    division_count = divisions.count()
    context = {'divisions':divisions,'division_count':division_count}
    return render(request,'configuration/division.html',context)


def create_division(request):
    form = DivisionForm()
    if request.method == 'POST' :
        form = DivisionForm(request.POST)
        if form.is_valid(): 
            form.save()
            return redirect('division')
    context = {'form':form, 'text':'Division'}
    return render(request, 'configuration/form.html', context)


def update_division(request,id):
    division = Division.objects.get(id=id)
    form = DivisionForm(instance=division)
    if request.method == 'POST' :
        form = DivisionForm(request.POST, instance=division)
        if form.is_valid() : 
            form.save()
            return redirect('division')
    context = {'form':form}
    return render(request, 'configuration/form.html', context)


def delete_division(request,id):
    division = Division.objects.get(id=id)
    if request.method == 'POST' :
        division.soft_deleted()
        return redirect('division')
    context = {'obj':division}
    return render(request,'configuration/delete.html',context)


def restore_division(request,id):
    division = Division.deleted_objects.get(id=id)
    if request.method == 'POST' :
        division.restore()
        return redirect('division')

    context = {'obj':division}
    return render(request,'configuration/restore.html',context)

# CRUD-R for PROGRAM

# ...
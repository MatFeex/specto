from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q

from .models import Criteria, HoldingGrid, HoldingGridCriteria
from .forms import CriteriaForm, HoldingGridForm, HoldingGridCriteriaForm
from datetime import datetime



# CRUD-R for 5S CRITERIA

def read_criteria(request):
    criterias = Criteria.objects.all()
    criteria_count = criterias.count()
    context = {'criterias':criterias,'criteria_count':criteria_count}
    return render(request,'criteria/criteria.html',context)


def read_deleted_criteria(request):
    criterias = Criteria.deleted_objects.all()
    criteria_count = criterias.count()
    context = {'criterias':criterias,'criteria_count':criteria_count}
    return render(request,'criteria/deleted_criteria.html',context)


def create_criteria(request):
    form = CriteriaForm()
    if request.method == 'POST' :
        form = CriteriaForm(request.POST)
        if form.is_valid(): 
            form.save()
            return redirect('criteria')
        else : messages.error(request, 'An error occurred while adding the criteria')
    context = {'form':form, 'text':'CREATE A NEW CRITERIA'}
    return render(request, 'form.html', context)


def update_criteria(request,criteria_id):
    criteria = Criteria.objects.get(id=criteria_id)
    form = CriteriaForm(instance=criteria)
    if request.method == 'POST' :
        form = CriteriaForm(request.POST, instance=criteria)
        if form.is_valid() : 
            form.save()
            return redirect('criteria')
        else : messages.error(request, 'An error occurred while updating the criteria')
    context = {'form':form, 'text':'UPDATE THE CRITERIA'}
    return render(request, 'form.html', context)


def delete_criteria(request,criteria_id):
    criteria = Criteria.objects.get(id=criteria_id)
    holding_grids = HoldingGrid.objects.filter(criteria_id=criteria_id)
    if request.method == 'POST' :
        criteria.soft_deleted()
        for item in holding_grids : item.soft_deleted()
        return redirect('criteria')
    context = {'obj':criteria}
    return render(request,'delete.html',context)


def restore_criteria(request,criteria_id):
    criteria = Criteria.deleted_objects.get(id=criteria_id)
    holding_grids = HoldingGrid.deleted_objects.filter(criteria_id=criteria_id)
    if request.method == 'POST' :
        criteria.restore()
        for item in holding_grids : item.restore()
        return redirect('criteria')
    context = {'obj':criteria}
    return render(request,'restore.html',context)


# CRUD-R for 5S / Holding grid

def read_five_s(request):
    five_ss = HoldingGrid.objects.all()
    five_s_count = five_ss.count()
    context = {'five_ss':five_ss,'five_s_count':five_s_count}
    return render(request,'five_s/five_s.html',context)


def read_specific_five_s(request,five_s_id):
    five_s = HoldingGrid.objects.get(id=five_s_id)
    criterias = Criteria.objects.all() # to display criterias
    five_s_criterias = HoldingGridCriteria.objects.filter(holding_grid_id=five_s_id) # ITEMS for the specific Holding Grid
    zip_criterias = zip(criterias,five_s_criterias) # zip to easy access in template
    context = {'five_s':five_s,'zip_criterias':zip_criterias}
    return render(request,'five_s/five_s_details.html',context)


def read_five_s_actions(request):
    five_s_criterias = HoldingGridCriteria.objects.filter(~Q(action='') & ~Q(action=None))
    context = {'five_s_criterias':five_s_criterias}
    return render(request,'five_s/five_s_actions.html',context)


def read_deleted_five_s(request):
    five_ss = HoldingGrid.deleted_objects.all()
    five_s_count = five_ss.count()
    context = {'five_ss':five_ss,'five_s_count':five_s_count}
    return render(request,'five_s/deleted_five_s.html',context)


def create_five_s(request):

    if request.method == 'POST' :

        # GET INPUTS
        criteria_ids = request.POST.getlist('criteria-id')
        responses = [True if x == '1' else False for x in request.POST.getlist('response')]
        comments = request.POST.getlist('comment')
        
        # Holding Grid/HoldingGridCriteria FORM
        five_s_form = HoldingGridForm(request.POST)

        if five_s_form.is_valid():
            
            # SAVE PARENT
            five_s_form.save()

            # CHILDS - Holding Grid_Item - ManyToMany  
            for i in range(len(criteria_ids)) : 
                HoldingGridCriteria.objects.create(criteria_id = criteria_ids[i],
                                        holding_grid_id = five_s_form.instance.id,
                                        response = responses[i],
                                        comment = comments[i],
                                        )

            return redirect('five-s')
        else : messages.error(request, 'An error occurred while creating the 5S - Holding Grid')

    else : 
        five_s_form = HoldingGridForm()
        five_s_criteria_form = HoldingGridCriteriaForm()

    criterias = Criteria.objects.all()
    context = {'five_s_form':five_s_form,'five_s_criteria_form':five_s_criteria_form,'text':'CREATE A NEW 5S HOLDING GRID','criterias':criterias}
    return render(request, 'five_s/five_s_form.html', context)


def update_five_s(request,five_s_id):
    five_s = HoldingGrid.objects.get(id=five_s_id)

    if request.method == 'POST' :

        # GET INPUTS
        criteria_ids = request.POST.getlist('criteria-id')
        responses = [True if x == '1' else False for x in request.POST.getlist('response')]
        comments = request.POST.getlist('comment')

        
        # Holding Grid FORM
        five_s_form = HoldingGridForm(request.POST, instance = five_s)

        if five_s_form.is_valid():

            # SAVE PARENT
            five_s_form.save()

            # Delete previous m2m CHILDS
            HoldingGridCriteria.objects.filter(holding_grid_id=five_s_id).delete()

            # NEW CHILDS - Holding Grid_Item - ManyToMany  
            for i in range(len(criteria_ids)) : 
                HoldingGridCriteria.objects.create(criteria_id = criteria_ids[i],
                                        holding_grid_id = five_s_form.instance.id,
                                        response = responses[i],
                                        comment = comments[i],
                                        )
            return redirect('five-s')

        else : messages.error(request, 'An error occurred while updating the Holding Grid')

    else : five_s_form = HoldingGridForm(instance=five_s)

    criterias = Criteria.objects.all() # to display criterias
    five_s_criterias = HoldingGridCriteria.objects.filter(holding_grid_id=five_s_id) # ITEMS for the specific Holding Grid
    zip_criterias = zip(criterias,five_s_criterias) # zip to easy access in template

    context = {'five_s_form':five_s_form,'zip_criterias':zip_criterias,'five_s':five_s}
    return render(request, 'five_s/five_s_update_form.html', context)


def delete_five_s(request,five_s_id):
    five_s = HoldingGrid.objects.get(id=five_s_id)
    if request.method == 'POST' :
        five_s.soft_deleted()
        return redirect('five_s')
    context = {'obj':five_s}
    return render(request,'five_s/delete.html',context)


def restore_five_s(request,five_s_id):

    five_s = HoldingGrid.deleted_objects.get(id=five_s_id)
    if request.method == 'POST' :
        five_s.restore()
        return redirect('five_s')
    context = {'obj':five_s}
    return render(request,'five_s/restore.html',context)






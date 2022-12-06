from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q

from .models import Passation, PassationAction, PassationStatus
from .forms import PassationForm
from datetime import datetime



# CRUD-R for PASSATION

def read_passation(request):
    passations = Passation.objects.all()
    context = {'passations':passations}
    return render(request,'passation/passation/passation.html',context)


def read_specific_passation(request,passation_id):
    passation = Passation.objects.get(id=passation_id)
    actions = PassationAction.objects.filter(passation_id=passation_id)
    statuses = []
    for action in actions : statuses.append(PassationStatus.objects.get(id = action.id).status)
    action_status = zip(actions,statuses)
    context = {'passation':passation,'action_status':action_status}
    return render(request,'passation/passation/passation_details.html',context)


def read_deleted_passation(request):
    passations = Passation.deleted_objects.all()
    passation_count = passations.count()
    context = {'passations':passations,'passation_count':passation_count}
    return render(request,'passation/passation/deleted_passation.html',context)


def create_passation(request):


    if request.method == 'POST' :

        # GET INPUTS
        msns = request.POST.getlist('msn')
        actions = request.POST.getlist('action')
        statuses = request.POST.getlist('status')
       
        
        # PASSATION FORM
        
        passation_form = PassationForm(request.POST)


        if passation_form.is_valid():

            # SAVE PARENT
            passation_form.save()

            # CHILDS - PASSATION_Action - ManyToMany  
            for i in range(len(actions)) : 
                new_action = PassationAction.objects.create(passation_id = passation_form.instance.id,msn = msns[i],action = actions[i])
                PassationStatus.objects.create(action = new_action, status = statuses[i])
            
            return redirect('passation')
        else : messages.error(request, 'An error occurred while creating the Passation')
    
    else : passation_form = PassationForm()

    context = {'passation_form':passation_form}
    return render(request, 'passation/passation/passation_form.html', context)



def update_passation(request,passation_id):

    passation = Passation.objects.get(id=passation_id)

    if request.method == 'POST' :

        # GET INPUTS
        msns = request.POST.getlist('msn')
        actions = request.POST.getlist('action')
        statuses = request.POST.getlist('status')
        
        # PASSATION FORM
        passation_form = PassationForm(request.POST, instance=passation)

        if passation_form.is_valid():

            # SAVE PARENT
            passation_form.save()

            # Delete previous CHILDS
            PassationAction.objects.filter(passation_id = passation_id).delete()


            # new CHILDS 
            for i in range(len(actions)) : 
                new_action = PassationAction.objects.create(passation = Passation.objects.get(id = passation_id),msn = msns[i],action = actions[i])
                PassationStatus.objects.create(action = new_action, status = statuses[i])
            
            return redirect('passation')
        else : messages.error(request, 'An error occurred while updating the PASSATION')
    else : passation_form = PassationForm(instance = passation)

    actions = PassationAction.objects.filter(passation_id=passation_id)
    statuses = []
    for action in actions : statuses.append(PassationStatus.objects.get(id = action.id).status)
    action_status = zip(actions,statuses)
    
    context = {'passation_form':passation_form, 'action_status':action_status}
    return render(request, 'passation/passation/passation_update_form.html', context)


def delete_passation(request,passation_id):
    passation = Passation.objects.get(id=passation_id)
    if request.method == 'POST' :
        passation.soft_deleted()
        return redirect('passation')
    context = {'obj':passation}
    return render(request,'passation/delete.html',context)


def restore_passation(request,passation_id):
    passation = Passation.deleted_objects.get(id=passation_id)
    if request.method == 'POST' :
        passation.restore()
        return redirect('passation')
    context = {'obj':passation}
    return render(request,'passation/restore.html',context)
from django.shortcuts import render, redirect
from .models import Vms, VmsItem
from configuration.models import VMS_Planning
from .forms import VmsForm
from django.contrib import messages
from datetime import datetime
from django.db.models import Q

   
# CRUD-R for VMS

def read_vms(request):
    vmss = Vms.objects.all()
    vms_count = vmss.count()
    context = {'vmss':vmss,'vms_count':vms_count}
    return render(request,'vms/vms/vms.html',context)


def read_specific_vms(request,vms_id):
    vms = Vms.objects.get(id=vms_id)
    vms_items = VmsItem.objects.filter(vms_id=vms_id) # ITEMS for the specific VMS
    context = {'vms':vms,'vms_items':vms_items}
    return render(request,'vms/vms/vms_details.html',context)

def read_vms_actions(request):
    vms_items = VmsItem.objects.filter(~Q(action='') & ~Q(action=None))
    context = {'vms_items':vms_items}
    return render(request,'vms/vms/vms_actions.html',context)

def read_deleted_vms(request):
    vmss = Vms.deleted_objects.all()
    vms_count = vmss.count()
    context = {'vmss':vmss,'vms_count':vms_count}
    return render(request,'vms/vms/deleted_vms.html',context)


def create_vms(request):

    if request.method == 'POST' :

        # GET INPUTS
        observations = request.POST.getlist('observation')
        condition_types = request.POST.getlist('condition_type')
        dialogue_answers = request.POST.getlist('dialogue_answer')
        action_types = request.POST.getlist('action_type')
        actions = request.POST.getlist('action')
        managers = request.POST.getlist('manager')
        delays = request.POST.getlist('delay')
        print(delays)
        
        # VMS FORM
        vms_form = VmsForm(request.POST)

        if vms_form.is_valid():

            # SAVE PARENT
            vms_form.save()

            # CHILDS - VMS_Item - ManyToMany  
            for i in range(len(observations)) : 
                VmsItem.objects.create( vms_id = vms_form.instance.id,
                                        observation = observations[i],
                                        condition_type = condition_types[i],
                                        dialogue_answer = dialogue_answers[i],
                                        action_type = action_types[i],
                                        action = actions[i],
                                        manager = managers[i],
                                        delay = delays[i],
                                        )
            try : 
                employee_visited_id = Vms.objects.get(id = vms_form.instance.id).employee.matricule
                planning_to_close = VMS_Planning.objects.filter(employee_visited_id = employee_visited_id).latest('created_at')
                planning_to_close.closed = True
                planning_to_close.save()
                return redirect('vms')
            except : messages.error(request, "The corresponding VMS Planning for the visited employee doesn't exist")
        else : messages.error(request, 'An error occurred while creating the VMS')
    
    else : vms_form = VmsForm()

    context = {'vms_form':vms_form,'today':str(datetime.now())[:10]}
    return render(request, 'vms/vms/vms_form.html', context)



def update_vms(request,vms_id):

    vms = Vms.objects.get(id=vms_id)

    if request.method == 'POST' :

        # GET INPUTS
        observations = request.POST.getlist('observation')
        condition_types = request.POST.getlist('condition_type')
        dialogue_answers = request.POST.getlist('dialogue_answer')
        action_types = request.POST.getlist('action_type')
        actions = request.POST.getlist('action')
        managers = request.POST.getlist('manager')
        delays = request.POST.getlist('delay')
        
        # VMS FORM
        vms_form = VmsForm(request.POST, instance=vms)

        if vms_form.is_valid():

            # SAVE PARENT
            vms_form.save()

            # Delete previous m2m CHILDS
            VmsItem.objects.filter(vms_id=vms_id).delete()

            # CHILDS - VMS_Item - ManyToMany  
            for i in range(len(observations)) : 
                VmsItem.objects.create( vms = Vms.objects.get(id = vms_id),
                                        observation = observations[i],
                                        condition_type = condition_types[i],
                                        dialogue_answer = dialogue_answers[i],
                                        action_type = action_types[i],
                                        action = actions[i],
                                        manager = managers[i],
                                        delay = delays[i],
                                        )
            return redirect('vms')
        else : messages.error(request, 'An error occurred while updating the VMS')
    else : vms_form = VmsForm(instance = vms)

    vms_items = VmsItem.objects.filter(vms_id=vms_id) # ITEMS for the specific VMS
    context = {'vms_form':vms_form,'today':str(datetime.now())[:10],'vms_items':vms_items}
    return render(request, 'vms/vms/vms_update_form.html', context)


def delete_vms(request,vms_id):
    vms = Vms.objects.get(id=vms_id)
    if request.method == 'POST' :
        vms.soft_deleted()
        return redirect('vms')
    context = {'obj':vms}
    return render(request,'vms/delete.html',context)


def restore_vms(request,vms_id):
    vms = Vms.deleted_objects.get(id=vms_id)
    if request.method == 'POST' :
        vms.restore()
        return redirect('vms')
    context = {'obj':vms}
    return render(request,'vms/restore.html',context)
from django.shortcuts import render, redirect
from .models import GembaService, GembaItem, Gemba, GembaItemItem
from .forms import GembaServiceForm, GembaServiceForm, GembaItemForm, GembaForm
from django.contrib import messages
from django.db.models import Q



# SPECTO VIEWS : VMQ

# CRUD-R for GEMBA SERVICE

def read_gemba_service(request):
    services = GembaService.objects.all()
    context = {'services':services}
    return render(request,'gemba/gemba_service/gemba_service.html',context)

def read_deleted_gemba_service(request):
    services = GembaService.deleted_objects.all()
    context = {'services':services}
    return render(request,'gemba/gemba_service/deleted_gemba_service.html',context)


def create_gemba_service(request):
    if request.method == 'POST' :
        form = GembaServiceForm(request.POST)
        if form.is_valid(): 
            form.save()
            return redirect('gemba-service')
        else : messages.error(request, 'An error occurred while adding the gemba service')
    else : form = GembaServiceForm()
    context = {'form':form, 'text':'CREATE A NEW GEMBA SERVICE'}
    return render(request, 'gemba/form.html', context)


def update_gemba_service(request,gemba_service_id):
    gemba_service = GembaService.objects.get(id=gemba_service_id)
    form = GembaServiceForm(instance=gemba_service)
    if request.method == 'POST' :
        form = GembaServiceForm(request.POST, instance=gemba_service)
        if form.is_valid() : 
            form.save()
            return redirect('gemba-service')
        else : messages.error(request, 'An error occurred while updating the gemba service')
    context = {'form':form, 'text':'UPDATE THE GEMBA SERVICE'}
    return render(request, 'gemba/form.html', context)


def delete_gemba_service(request,gemba_service_id):
    gemba_service = GembaService.objects.get(id=gemba_service_id)
    gemba_items = GembaItem.objects.filter(gemba_service_id=gemba_service_id)
    if request.method == 'POST' :
        gemba_service.soft_deleted()
        for item in gemba_items : item.soft_deleted()
        return redirect('gemba-service')
    context = {'obj':gemba_service}
    return render(request,'gemba/delete.html',context)


def restore_gemba_service(request,gemba_service_id):
    gemba_service = GembaService.deleted_objects.get(id=gemba_service_id)
    gemba_items = GembaItem.deleted_objects.filter(gemba_service_id=gemba_service_id)
    if request.method == 'POST' :
        gemba_service.restore()
        for item in gemba_items : item.restore()
        return redirect('gemba-service')
    context = {'obj':gemba_service}
    return render(request,'gemba/restore.html',context)


# CRUD-R for GEMBA ITEM

def read_gemba_item(request, gemba_service_id):
    gemba_items = GembaItem.objects.all().filter(gemba_service_id=gemba_service_id)
    context = {'gemba_items':gemba_items,'gemba_service_id':gemba_service_id}
    return render(request,'gemba/gemba_item/gemba_item.html',context)


def read_deleted_gemba_item(request, gemba_service_id):
    gemba_items = GembaItem.deleted_objects.all().filter(gemba_service_id=gemba_service_id)
    item_count = gemba_items.count()
    context = {'gemba_items':gemba_items,'item_count':item_count,'gemba_service_id':gemba_service_id}
    return render(request,'gemba/gemba_item/deleted_gemba_item.html',context)


def create_gemba_item(request, gemba_service_id):
    form = GembaItemForm()
    if request.method == 'POST' :
        form = GembaItemForm(request.POST)
        if form.is_valid() : 
            form.gemba_service_id = gemba_service_id
            f = form.save(commit=False)
            f.gemba_service_id = gemba_service_id
            f.save()
            return redirect(f'/gemba/gemba-service/{gemba_service_id}/gemba-item/')
        else : messages.error(request, 'An error occurred while adding the gemba item')
    context = {'form':form, 'text':'CREATE A NEW GEMBA ITEM'}
    return render(request, 'gemba/form.html', context)


def update_gemba_item(request,gemba_service_id, gemba_item_id):
    item = GembaItem.objects.filter(gemba_service_id=gemba_service_id).get(id=gemba_item_id)
    if request.method == 'POST' :
        form = GembaItemForm(request.POST, instance=item)
        if form.is_valid() : 
            form.gemba_service_id = gemba_service_id
            f = form.save(commit=False)
            f.gemba_service_id = gemba_service_id
            f.save()
            return redirect(f'/gemba/gemba-service/{gemba_service_id}/gemba-item/')
        else : messages.error(request, 'An error occurred while updating the gemba item')
    else : form = GembaItemForm(instance=item)
    context = {'form':form, 'text':'UPDATE THE GEMBA ITEM'}
    return render(request, 'gemba/form.html', context)


def delete_gemba_item(request,gemba_service_id, gemba_item_id):
    item = GembaItem.objects.filter(gemba_service_id=gemba_service_id).get(id=gemba_item_id)
    if request.method == 'POST' :
        item.soft_deleted()
        return redirect(f'/gemba/gemba-service/{gemba_service_id}/gemba-item/')
    context = {'obj':item}
    return render(request,'gemba/delete.html',context)


def restore_gemba_item(request,gemba_service_id, gemba_item_id):
    item = GembaItem.deleted_objects.filter(gemba_service_id=gemba_service_id).get(id=gemba_item_id)
    if request.method == 'POST' :
        item.restore()
        return redirect(f'/gemba/gemba-service/{gemba_service_id}/gemba-item/')
    context = {'obj':item}
    return render(request,'gemba/restore.html',context)
    
# CRUD-R for GEMBA

def read_gemba(request):
    gembas = Gemba.objects.all()
    context = {'gembas':gembas}
    return render(request,'gemba/gemba/gemba.html',context)


def read_specific_gemba(request,gemba_id):
    gemba = Gemba.objects.get(id=gemba_id)
    gemba_items = GembaItem.objects.all() # to display gemba_items
    gemba_gemba_items = GembaItemItem.objects.filter(gemba_id=gemba_id) # ITEMS for the specific VMQ
    zip_gemba_items = zip(gemba_items,gemba_gemba_items) # zip to easy access in template
    context = {'gemba':gemba,'zip_gemba_items':zip_gemba_items}
    return render(request,'gemba/gemba/gemba_details.html',context)

def read_gemba_actions(request):
    gemba_gemba_items = GembaItemItem.objects.filter(~Q(action='') & ~Q(action=None))
    context = {'gemba_gemba_items':gemba_gemba_items}
    return render(request,'gemba/gemba/gemba_actions.html',context)

def read_deleted_gemba(request):
    gembas = Gemba.deleted_objects.all()
    context = {'gembas':gembas}
    return render(request,'gemba/gemba/deleted_gemba.html',context)


def create_gemba(request):

    if request.method == 'POST' :

        # GET INPUTS
        gemba_item_ids = request.POST.getlist('gemba-item-id')
        answers = request.POST.getlist('answer')
        problems = request.POST.getlist('problem')
        actions = request.POST.getlist('action')
        
        # GEMBA FORM  
        gemba_form = GembaForm(request.POST)

        if gemba_form.is_valid():

            # SAVE PARENT
            gemba_form.save()

            # CHILDS - VMQ_GembaItem - ManyToMany  
            for i in range(len(gemba_item_ids)) : 
                GembaItemItem.objects.create( gemba_item = GembaItem.objects.get(id=gemba_item_ids[i]),
                                        gemba = Gemba.objects.get(id = gemba_form.instance.id),
                                        answer = answers[i],
                                        problem = problems[i],
                                        action = actions[i],
                                        )
            return redirect('gemba')

        else : messages.error(request, 'An error occurred while creating the Gemba Walk')

    else : gemba_form = GembaForm()

    gemba_items = GembaItem.objects.all()
    context = {'gemba_form':gemba_form,'text':'CREATE A NEW GEMBA WALK','gemba_items':gemba_items}
    return render(request, 'gemba/gemba/gemba_form.html', context)


def update_gemba(request,gemba_id):
    gemba = Gemba.objects.get(id=gemba_id)

    if request.method == 'POST' :

        # GET INPUTS
        gemba_item_ids = request.POST.getlist('gemba-item-id')
        answers = request.POST.getlist('answer')
        problems = request.POST.getlist('problem')
        actions = request.POST.getlist('action')
        
        # GEMBA FORM  
        gemba_form = GembaForm(request.POST, instance = gemba)

        if gemba_form.is_valid():

            # SAVE PARENT
            gemba_form.save()

            # Delete previous m2m CHILDS
            GembaItemItem.objects.filter(gemba_id=gemba_id).delete()

            # NEW CHILDS - VMQ_GembaItem - ManyToMany  
            for i in range(len(gemba_item_ids)) : 
                GembaItemItem.objects.create( gemba_item = GembaItem.objects.get(id=gemba_item_ids[i]),
                                        gemba = Gemba.objects.get(id = gemba_form.instance.id),
                                        answer = answers[i],
                                        problem = problems[i],
                                        action = actions[i],
                                        )
            return redirect('gemba')

        else : messages.error(request, 'An error occurred while updating the Gemba Walk')

    else : gemba_form = GembaForm(instance=gemba)

    gemba_items = GembaItem.objects.all() # to display gemba_items
    gemba_gemba_items = GembaItemItem.objects.filter(gemba_id=gemba_id) # ITEMS for the specific VMQ
    zip_gemba_items = zip(gemba_items,gemba_gemba_items) # zip to easy access in template

    context = {'gemba_form':gemba_form,'zip_gemba_items':zip_gemba_items}
    return render(request, 'gemba/gemba/gemba_update_form.html', context)


def delete_gemba(request,gemba_id):
    gemba = Gemba.objects.get(id=gemba_id)
    if request.method == 'POST' :
        gemba.soft_deleted()
        return redirect('gemba')
    context = {'obj':'GEMBA '+ str(gemba.id)}
    return render(request,'gemba/delete.html',context)


def restore_gemba(request,gemba_id):
    gemba = Gemba.deleted_objects.get(id=gemba_id)
    if request.method == 'POST' :
        gemba.restore()
        return redirect('gemba')
    context = {'obj':gemba}
    return render(request,'gemba/restore.html',context)
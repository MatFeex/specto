from django.shortcuts import render, redirect
from .models import Theme, Item, Vmq, VmqItem
from configuration.models import VMQ_Planning
from .forms import ThemeForm, ItemForm, VmqForm
from django.contrib import messages
from django.db.models import Q
from datetime import datetime
import pytz

# SPECTO VIEWS : VMQ

# CRUD-R for THEME

def read_theme(request):
    themes = Theme.objects.all()
    theme_count = themes.count()
    context = {'themes':themes,'theme_count':theme_count}
    return render(request,'vmq/theme/theme.html',context)


def read_deleted_theme(request):
    themes = Theme.deleted_objects.all()
    theme_count = themes.count()
    context = {'themes':themes,'theme_count':theme_count}
    return render(request,'vmq/theme/deleted_theme.html',context)


def create_theme(request):
    form = ThemeForm()
    if request.method == 'POST' :
        form = ThemeForm(request.POST)
        if form.is_valid(): 
            form.save()
            return redirect('theme')
        else : messages.error(request, 'An error occurred while adding the theme')
    context = {'form':form, 'text':'CREATE A NEW THEME'}
    return render(request, 'vmq/form.html', context)


def update_theme(request,theme_id):
    theme = Theme.objects.get(id=theme_id)
    form = ThemeForm(instance=theme)
    if request.method == 'POST' :
        form = ThemeForm(request.POST, instance=theme)
        if form.is_valid() : 
            form.save()
            return redirect('theme')
        else : messages.error(request, 'An error occurred while updating the theme')
    context = {'form':form, 'text':'UPDATE THE THEME'}
    return render(request, 'vmq/form.html', context)


def delete_theme(request,theme_id):
    theme = Theme.objects.get(id=theme_id)
    items = Item.objects.filter(theme_id=theme_id)
    if request.method == 'POST' :
        theme.soft_deleted()
        for item in items : item.soft_deleted()
        return redirect('theme')
    context = {'obj':theme}
    return render(request,'vmq/delete.html',context)


def restore_theme(request,theme_id):
    theme = Theme.deleted_objects.get(id=theme_id)
    items = Item.deleted_objects.filter(theme_id=theme_id)
    if request.method == 'POST' :
        theme.restore()
        for item in items : item.restore()
        return redirect('theme')
    context = {'obj':theme}
    return render(request,'vmq/restore.html',context)


# CRUD-R for ITEM

def read_item(request, theme_id):
    items = Item.objects.all().filter(theme_id=theme_id)
    item_count = items.count()
    context = {'items':items,'item_count':item_count,'theme_id':theme_id}
    return render(request,'vmq/item/item.html',context)


def read_deleted_item(request, theme_id):
    items = Item.deleted_objects.all().filter(theme_id=theme_id)
    item_count = items.count()
    context = {'items':items,'item_count':item_count,'theme_id':theme_id}
    return render(request,'vmq/item/deleted_item.html',context)


def create_item(request, theme_id):
    form = ItemForm()
    if request.method == 'POST' :
        form = ItemForm(request.POST)
        if form.is_valid() : 
            form.theme_id = theme_id
            f = form.save(commit=False)
            f.theme_id = theme_id
            f.save()
            return redirect(f'/vmq/theme/{theme_id}/item/')
        else : messages.error(request, 'An error occurred while adding the item')
    context = {'form':form, 'text':'CREATE A NEW ITEM'}
    return render(request, 'vmq/form.html', context)


def update_item(request,theme_id, item_id):
    item = Item.objects.all().filter(theme_id=theme_id).get(id=item_id)
    form = ItemForm(instance=item)
    if request.method == 'POST' :
        form = ItemForm(request.POST, instance=item)
        if form.is_valid() : 
            form.theme_id = theme_id
            f = form.save(commit=False)
            f.theme_id = theme_id
            f.save()
            return redirect(f'/vmq/theme/{theme_id}/item/')
        else : messages.error(request, 'An error occurred while updating the item')
    context = {'form':form, 'text':'UPDATE THE ITEM'}
    return render(request, 'vmq/form.html', context)


def delete_item(request,theme_id, item_id):
    item = Item.objects.all().filter(theme_id=theme_id).get(id=item_id)
    if request.method == 'POST' :
        item.soft_deleted()
        return redirect(f'/vmq/theme/{theme_id}/item/')
    context = {'obj':item}
    return render(request,'vmq/delete.html',context)


def restore_item(request,theme_id, item_id):
    item = Item.deleted_objects.all().filter(theme_id=theme_id).get(id=item_id)
    if request.method == 'POST' :
        item.restore()
        return redirect(f'/vmq/theme/{theme_id}/item/')
    context = {'obj':item}
    return render(request,'vmq/restore.html',context)
    
# CRUD-R for VMQ

def read_vmq(request):
    vmqs = Vmq.objects.all()
    vmq_count = vmqs.count()
    context = {'vmqs':vmqs,'vmq_count':vmq_count}
    return render(request,'vmq/vmq/vmq.html',context)


def read_specific_vmq(request,vmq_id):
    vmq = Vmq.objects.get(id=vmq_id)
    items = Item.objects.all() # to display items
    vmq_items = VmqItem.objects.filter(vmq_id=vmq_id) # ITEMS for the specific VMQ
    zip_items = zip(items,vmq_items) # zip to easy access in template
    context = {'vmq':vmq,'zip_items':zip_items}
    return render(request,'vmq/vmq/vmq_details.html',context)


def read_vmq_actions(request):
    vmq_items = VmqItem.objects.filter(~Q(action='') & ~Q(action=None))
    context = {'vmq_items':vmq_items}
    return render(request,'vmq/vmq/vmq_actions.html',context)


def read_deleted_vmq(request):
    vmqs = Vmq.deleted_objects.all()
    vmq_count = vmqs.count()
    context = {'vmqs':vmqs,'vmq_count':vmq_count}
    return render(request,'vmq/vmq/deleted_vmq.html',context)


def create_vmq(request):

    if request.method == 'POST' :

        # GET INPUTS
        item_ids = request.POST.getlist('item-id')
        results = request.POST.getlist('result')
        types = request.POST.getlist('type')
        comments = request.POST.getlist('comment')
        actions = request.POST.getlist('action')
        
        # VMQ FORM
        vmq_form = VmqForm(request.POST)

        if vmq_form.is_valid():
            try :
                # SAVE PARENT
                vmq_form.save()

                # CHILDS - VMQ_Item - ManyToMany  
                for i in range(len(item_ids)) : 
                    VmqItem.objects.create( item = Item.objects.get(id=item_ids[i]),
                                            vmq = Vmq.objects.get(id = vmq_form.instance.id),
                                            result = results[i],
                                            type = types[i],
                                            comment = comments[i],
                                            action = actions[i],
                                            )
                
                planning_to_close = VMQ_Planning.objects.filter(vmq_employee_visited_id = vmq_form.instance.employee.matricule, closed = False).latest('created_at')
                planning_to_close.closed = True
                planning_to_close.save()
                return redirect('vmq')
            except : messages.error(request, "Employee already visited or corresponding VMQ Planning inexistent")
        else : messages.error(request, 'An error occurred while creating the VMQ')

    else : vmq_form = VmqForm()

    items = Item.objects.all()
    context = {'vmq_form':vmq_form,'text':'CREATE A NEW VMQ','items':items}
    return render(request, 'vmq/vmq/vmq_form.html', context)


def update_vmq(request,vmq_id):
    vmq = Vmq.objects.get(id=vmq_id)

    if request.method == 'POST' :

        # GET INPUTS
        item_ids = request.POST.getlist('item-id')
        results = request.POST.getlist('result')
        types = request.POST.getlist('type')
        comments = request.POST.getlist('comment')
        actions = request.POST.getlist('action')

        
        # VMQ FORM
        vmq_form = VmqForm(request.POST, instance = vmq)

        if vmq_form.is_valid():

            # SAVE PARENT
            vmq_form.save()

            # Delete previous m2m CHILDS
            VmqItem.objects.filter(vmq_id=vmq_id).delete()

            # NEW CHILDS - VMQ_Item - ManyToMany  
            for i in range(len(item_ids)) : 
                VmqItem.objects.create( item = Item.objects.get(id=item_ids[i]),
                                        vmq = Vmq.objects.get(id = vmq_form.instance.id),
                                        result = results[i],
                                        type = types[i],
                                        comment = comments[i],
                                        action = actions[i],
                                        )
            return redirect('vmq')

        else : messages.error(request, 'An error occurred while updating the VMQ')

    else : vmq_form = VmqForm(instance=vmq)


    items = Item.objects.all() # to display items
    vmq_items = VmqItem.objects.filter(vmq_id=vmq_id) # ITEMS for the specific VMQ
    zip_items = zip(items,vmq_items) # zip to easy access in template

    context = {'vmq_form':vmq_form,'zip_items':zip_items}
    return render(request, 'vmq/vmq/vmq_update_form.html', context)


def delete_vmq(request,vmq_id):
    vmq = Vmq.objects.get(id=vmq_id)
    if request.method == 'POST' :
        vmq.soft_deleted()
        return redirect('vmq')
    context = {'obj':vmq}
    return render(request,'vmq/delete.html',context)


def restore_vmq(request,vmq_id):

    vmq = Vmq.deleted_objects.get(id=vmq_id)
    if request.method == 'POST' :
        vmq.restore()
        return redirect('vmq')
    context = {'obj':vmq}
    return render(request,'vmq/restore.html',context)


# VMQ KPI
def select_range(request):
    return render(request,'vmq/vmq-kpi/vmq_kpi_date_range.html')

def vmq_kpi(request):

    date_stop = datetime.now().date()
    date_start = datetime(datetime.now().year,datetime.now().month,1).date()

    if request.method == 'POST':
            date_start = request.POST.get('date_start')
            date_stop = request.POST.get('date_stop')


    vmqs_kpi = VmqItem.objects.filter(vmq__created_at__range = (date_start,date_stop)).exclude(action='')
    item_action_list = [i.item for i in vmqs_kpi]
    themes_action_list = [i.item.theme for i in vmqs_kpi]

    vmq_kpi_item = {i.name:item_action_list.count(i) for i in item_action_list}
    vmq_kpi_theme = {i.name:themes_action_list.count(i) for i in themes_action_list}
    print(list(vmq_kpi_theme.keys()))
    context = {
        'vmqs_kpi':vmqs_kpi,'date_start':date_start, 'date_stop':date_stop,'vmq_kpi_item':vmq_kpi_item,
        'vmq_kpi_theme':vmq_kpi_theme,'themeLabels':list(vmq_kpi_theme.keys()),'themeData':list(vmq_kpi_theme.values()),
        'itemLabels':list(vmq_kpi_item.keys()),'itemData':list(vmq_kpi_item.values())
        }
    return render(request,'vmq/vmq-kpi/vmq_kpi.html',context)



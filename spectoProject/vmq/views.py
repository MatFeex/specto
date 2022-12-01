from django.shortcuts import render, redirect
from .models import Theme, Item, Vmq, VmqItem, QualityReference, Employee
from configuration.models import VMQ_Planning
from .forms import ThemeForm, ItemForm, VmqForm, QualityReferenceForm, VmqItemForm
from django.contrib import messages
from django.db.models import Q
from datetime import datetime

from .decorators import allowed_users

# SPECTO VIEWS : VMQ

# CRUD-R for QUALITY REFERENCE

def read_quality_reference(request):
    quality_references = QualityReference.objects.all()
    quality_reference_count = quality_references.count()
    context = {'quality_references':quality_references,'quality_reference_count':quality_reference_count}
    return render(request,'vmq/quality_reference/quality_reference.html',context)


def read_deleted_quality_reference(request):
    quality_references = QualityReference.deleted_objects.all()
    quality_reference_count = quality_references.count()
    context = {'quality_references':quality_references,'quality_reference_count':quality_reference_count}
    return render(request,'vmq/quality_reference/deleted_quality_reference.html',context)


def create_quality_reference(request):
    form = QualityReferenceForm()
    if request.method == 'POST' :
        form = QualityReferenceForm(request.POST)
        if form.is_valid(): 
            form.save()
            return redirect('quality-reference')
        else : messages.error(request, 'An error occurred while adding the quality_reference')
    context = {'form':form, 'text':'CREATE A NEW THEME'}
    return render(request, 'vmq/form.html', context)


def update_quality_reference(request,quality_reference_id):
    quality_reference = QualityReference.objects.get(id=quality_reference_id)
    form = QualityReferenceForm(instance=quality_reference)
    if request.method == 'POST' :
        form = QualityReferenceForm(request.POST, instance=quality_reference)
        if form.is_valid() : 
            form.save()
            return redirect('quality-reference')
        else : messages.error(request, 'An error occurred while updating the quality_reference')
    context = {'form':form, 'text':'UPDATE THE THEME'}
    return render(request, 'vmq/form.html', context)


def delete_quality_reference(request,quality_reference_id):
    quality_reference = QualityReference.objects.get(id=quality_reference_id)
    items = Item.objects.filter(quality_reference_id=quality_reference_id)
    if request.method == 'POST' :
        quality_reference.soft_deleted()
        for item in items : item.soft_deleted()
        return redirect('quality-reference')
    context = {'obj':quality_reference}
    return render(request,'vmq/delete.html',context)


def restore_quality_reference(request,quality_reference_id):
    quality_reference = QualityReference.deleted_objects.get(id=quality_reference_id)
    items = Item.deleted_objects.filter(quality_reference_id=quality_reference_id)
    if request.method == 'POST' :
        quality_reference.restore()
        for item in items : item.restore()
        return redirect('quality-reference')
    context = {'obj':quality_reference}
    return render(request,'vmq/restore.html',context)


# CRUD-R for THEME

def read_theme(request, quality_reference_id):
    themes = Theme.objects.all().filter(quality_reference_id=quality_reference_id)
    theme_count = themes.count()
    context = {'themes':themes,'theme_count':theme_count, 'quality_reference_id':quality_reference_id}
    return render(request,'vmq/theme/theme.html',context)


def read_deleted_theme(request, quality_reference_id):
    themes = Theme.deleted_objects.all().filter(quality_reference_id=quality_reference_id)
    theme_count = themes.count()
    context = {'themes':themes,'theme_count':theme_count,'quality_reference_id':quality_reference_id}
    return render(request,'vmq/theme/deleted_theme.html',context)


def create_theme(request, quality_reference_id):
    form = ThemeForm()
    if request.method == 'POST' :
        form = ThemeForm(request.POST)
        if form.is_valid(): 
            form.quality_reference_id = quality_reference_id
            f = form.save(commit=False)
            f.quality_reference_id = quality_reference_id
            f.save()
            return redirect(f'/vmq/quality_reference/{quality_reference_id}/theme/')
        else : messages.error(request, 'An error occurred while adding the theme')
    context = {'form':form, 'text':'CREATE A NEW THEME','quality_reference_id':quality_reference_id}
    return render(request, 'vmq/form.html', context)


def update_theme(request,quality_reference_id,theme_id):
    theme = Theme.objects.get(id=theme_id)
    form = ThemeForm(instance=theme)
    if request.method == 'POST' :
        form = ThemeForm(request.POST, instance=theme)
        if form.is_valid() : 
            form.quality_reference_id = quality_reference_id
            f = form.save(commit=False)
            f.quality_reference_id = quality_reference_id
            f.save()
            return redirect(f'/vmq/quality_reference/{quality_reference_id}/theme/')
        else : messages.error(request, 'An error occurred while updating the theme')
    context = {'form':form, 'text':'UPDATE THE THEME','quality_reference_id':quality_reference_id}
    return render(request, 'vmq/form.html', context)


def delete_theme(request,quality_reference_id,theme_id):
    theme = Theme.objects.get(id=theme_id)
    items = Item.objects.filter(theme_id=theme_id)
    if request.method == 'POST' :
        theme.soft_deleted()
        for item in items : item.soft_deleted()
        return redirect(f'/vmq/quality_reference/{quality_reference_id}/theme/')
    context = {'obj':theme,'quality_reference_id':quality_reference_id}
    return render(request,'vmq/delete.html',context)


def restore_theme(request,quality_reference_id,theme_id):
    theme = Theme.deleted_objects.get(id=theme_id)
    items = Item.deleted_objects.filter(theme_id=theme_id)
    if request.method == 'POST' :
        theme.restore()
        for item in items : item.restore()
        return redirect('theme')
    context = {'obj':theme,'quality_reference_id':quality_reference_id}
    return render(request,'vmq/restore.html',context)


# CRUD-R for ITEM

def read_item(request, quality_reference_id, theme_id):
    items = Item.objects.all().filter(theme_id=theme_id)
    item_count = items.count()
    context = {'items':items,'item_count':item_count,'theme_id':theme_id,'quality_reference_id':quality_reference_id}
    return render(request,'vmq/item/item.html',context)


def read_deleted_item(request, quality_reference_id, theme_id):
    items = Item.deleted_objects.all().filter(theme_id=theme_id)
    item_count = items.count()
    context = {'items':items,'item_count':item_count,'theme_id':theme_id,'quality_reference_id':quality_reference_id}
    return render(request,'vmq/item/deleted_item.html',context)


def create_item(request, quality_reference_id, theme_id):
    form = ItemForm()
    if request.method == 'POST' :
        form = ItemForm(request.POST)
        if form.is_valid() : 
            form.theme_id = theme_id
            f = form.save(commit=False)
            f.theme_id = theme_id
            f.save()
            return redirect(f'/vmq/quality_reference/{quality_reference_id}/theme/{theme_id}/item/')
        else : messages.error(request, 'An error occurred while adding the item')
    context = {'form':form, 'text':'CREATE A NEW ITEM','quality_reference_id':quality_reference_id}
    return render(request, 'vmq/form.html', context)


def update_item(request,quality_reference_id, theme_id, item_id):
    item = Item.objects.all().filter(theme_id=theme_id).get(id=item_id)
    form = ItemForm(instance=item)
    if request.method == 'POST' :
        form = ItemForm(request.POST, instance=item)
        if form.is_valid() : 
            form.theme_id = theme_id
            f = form.save(commit=False)
            f.theme_id = theme_id
            f.save()
            return redirect(f'/vmq/quality_reference/{quality_reference_id}/theme/{theme_id}/item/')
        else : messages.error(request, 'An error occurred while updating the item')
    context = {'form':form, 'text':'UPDATE THE ITEM','quality_reference_id':quality_reference_id}
    return render(request, 'vmq/form.html', context)


def delete_item(request,quality_reference_id, theme_id, item_id):
    item = Item.objects.all().filter(theme_id=theme_id).get(id=item_id)
    if request.method == 'POST' :
        item.soft_deleted()
        return redirect(f'/vmq/quality_reference/{quality_reference_id}/theme/{theme_id}/item/')
    context = {'obj':item,'quality_reference_id':quality_reference_id}
    return render(request,'vmq/delete.html',context)


def restore_item(request,quality_reference_id, theme_id, item_id):
    item = Item.deleted_objects.all().filter(theme_id=theme_id).get(id=item_id)
    if request.method == 'POST' :
        item.restore()
        return redirect(f'/vmq/quality_reference/{quality_reference_id}/theme/{theme_id}/item/')
    context = {'obj':item, 'quality_reference_id':quality_reference_id}
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


@allowed_users(allowed_roles=['User','administrators','add_vmq_group'])
def create_vmq(request):
    try :

        username_matricule = 80197

        # GET latest planning dates
        latest_planning = VMQ_Planning.objects.latest('created_at')
        latest_month = latest_planning.month
        latest_year = latest_planning.year
        # GET employees list FROM latest planning
        latest_employee_visited_mat = list(VMQ_Planning.objects.filter(closed=False,month=latest_month,year=latest_year,vmq_employee_qualified=username_matricule).values_list('vmq_employee_visited', flat=True))
        latest_employee_visited = Employee.objects.filter(matricule__in = latest_employee_visited_mat)
    except : messages.error(request, "No VMQ planning resgistered : please generate one before creating a VMQ")

    if request.method == 'POST' :

        # GET INPUTS
        item_ids = request.POST.getlist('item-id')
        results = request.POST.getlist('result')
        types = request.POST.getlist('type')
        comments = request.POST.getlist('comment')
        actions = request.POST.getlist('action')
        defer_immediates = request.POST.getlist('defer_immediate')
        responsibles = request.POST.getlist('responsible')
        dates = request.POST.getlist('date')
        
        # VMQ/VmqItem FORM
        vmq_form = VmqForm(request.POST)
        vmq_item_form = VmqItemForm(request.POST)

        if vmq_form.is_valid():
            try :
                # SAVE PARENT
                visited_mat = request.POST.get('employee')
                vmq_form.employee = visited_mat
                f = vmq_form.save(commit=False)
                f.employee_id = visited_mat
                f.workshop_id = Employee.objects.get(matricule = visited_mat).workshop.id
                f.save()

                # CHILDS - VMQ_Item - ManyToMany  
                for i in range(len(item_ids)) : 
                    VmqItem.objects.create( item_id = item_ids[i],
                                            vmq_id = vmq_form.instance.id,
                                            result = results[i],
                                            type = types[i],
                                            comment = comments[i],
                                            action = actions[i],
                                            defer_immediate= defer_immediates[i],
                                            responsible_id = responsibles[i],
                                            date = dates[i],
                                            )
                
                planning_to_close = VMQ_Planning.objects.filter(vmq_employee_visited_id = vmq_form.instance.employee.matricule, closed = False).latest('created_at')
                planning_to_close.closed = True
                planning_to_close.save()
                return redirect('vmq')
            except : messages.error(request, "Employee already visited or corresponding VMQ Planning inexistent")
        else : messages.error(request, 'An error occurred while creating the VMQ')

    else : 
        vmq_form = VmqForm()
        vmq_item_form = VmqItemForm()

    latest_quality_ref_id = QualityReference.objects.latest('id').id
    items = Item.objects.filter(theme__quality_reference = latest_quality_ref_id)
    context = {'vmq_form':vmq_form,'vmq_item_form':vmq_item_form,'text':'CREATE A NEW VMQ','items':items, 'latest_employee_visited':latest_employee_visited}
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

    context = {'vmq_form':vmq_form,'zip_items':zip_items,'vmq':vmq}
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
    context = {
        'vmqs_kpi':vmqs_kpi,'date_start':date_start, 'date_stop':date_stop,'vmq_kpi_item':vmq_kpi_item,
        'vmq_kpi_theme':vmq_kpi_theme,'themeLabels':list(vmq_kpi_theme.keys()),'themeData':list(vmq_kpi_theme.values()),
        'itemLabels':list(vmq_kpi_item.keys()),'itemData':list(vmq_kpi_item.values())
        }
    return render(request,'vmq/vmq-kpi/vmq_kpi.html',context)



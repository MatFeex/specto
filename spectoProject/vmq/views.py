from django.shortcuts import render, redirect
from .models import Theme, Item
from .forms import ThemeForm, ItemForm


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
    context = {'form':form, 'text':'Theme'}
    return render(request, 'vmq/form.html', context)


def update_theme(request,theme_id):
    theme = Theme.objects.get(id=theme_id)
    form = ThemeForm(instance=theme)
    if request.method == 'POST' :
        form = ThemeForm(request.POST, instance=theme)
        if form.is_valid() : 
            form.save()
            return redirect('theme')
    context = {'form':form}
    return render(request, 'vmq/form.html', context)


def delete_theme(request,theme_id):
    theme = Theme.objects.get(id=theme_id)
    if request.method == 'POST' :
        theme.soft_deleted()
        return redirect('theme')
    context = {'obj':theme}
    return render(request,'vmq/delete.html',context)


def restore_theme(request,theme_id):
    theme = Theme.deleted_objects.get(id=theme_id)
    if request.method == 'POST' :
        theme.restore()
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
        if form.is_valid(): 
            form.save()
            return redirect(f'/vmq/theme/{theme_id}/item/')
    context = {'form':form, 'text':'Item'}
    return render(request, 'vmq/form.html', context)


def update_item(request,theme_id, item_id):
    item = Item.objects.all().filter(theme_id=theme_id).get(id=item_id)
    form = ItemForm(instance=item)
    if request.method == 'POST' :
        form = ItemForm(request.POST, instance=item)
        if form.is_valid() : 
            form.save()
            return redirect(f'/vmq/theme/{theme_id}/item/')
    context = {'form':form}
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
    
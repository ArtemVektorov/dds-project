from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Sum
from .models import CashFlowRecord, Type, Status, Category, Subcategory
from .forms import CashFlowForm
from .filters import CashFlowFilter


def main_page(request):
    queryset = CashFlowRecord.objects.all().select_related(
        'status', 'type', 'category', 'subcategory'
    )

    filterset = CashFlowFilter(request.GET, queryset=queryset)
    records = filterset.qs.order_by('-date', '-created_at')

    total_income = records.filter(type__name='Пополнение').aggregate(total=Sum('amount'))['total'] or 0
    total_expense = records.filter(type__name='Списание').aggregate(total=Sum('amount'))['total'] or 0
    balance = total_income - total_expense

    context = {
        'filter': filterset,
        'records': records,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
    }
    return render(request, 'core/main.html', context)


# --- Записи ДДС ---

def record_create(request):
    if request.method == 'POST':
        form = CashFlowForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Запись успешно создана.')
            return redirect('main')
    else:
        form = CashFlowForm()

    return render(request, 'core/record_form.html', {'form': form, 'title': 'Новая запись ДДС'})


def record_edit(request, pk):
    record = get_object_or_404(CashFlowRecord, pk=pk)
    if request.method == 'POST':
        form = CashFlowForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Запись успешно обновлена.')
            return redirect('main')
    else:
        form = CashFlowForm(instance=record)

    return render(request, 'core/record_form.html', {'form': form, 'title': 'Редактирование записи'})


def record_delete(request, pk):
    record = get_object_or_404(CashFlowRecord, pk=pk)
    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Запись успешно удалена.')
        return redirect('main')

    return render(request, 'core/record_confirm_delete.html', {'record': record})


# --- AJAX ---

from django.http import JsonResponse

def load_categories(request):
    type_id = request.GET.get('type_id')
    if type_id:
        categories = Category.objects.filter(type_id=type_id).order_by('name')
        return JsonResponse(list(categories.values('id', 'name')), safe=False)
    return JsonResponse([], safe=False)


def load_subcategories(request):
    category_id = request.GET.get('category_id')
    if category_id:
        subcats = Subcategory.objects.filter(category_id=category_id).order_by('name')
        return JsonResponse(list(subcats.values('id', 'name')), safe=False)
    return JsonResponse([], safe=False)


# --- Справочники: страница списка ---

def references_page(request):
    context = {
        'types': Type.objects.all(),
        'statuses': Status.objects.all(),
        'categories': Category.objects.select_related('type').all(),
        'subcategories': Subcategory.objects.select_related('category__type').all(),
    }
    return render(request, 'core/references.html', context)


# --- Type ---

def add_type(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            Type.objects.create(name=name)
            messages.success(request, 'Тип успешно добавлен.')
    return redirect('references')


def delete_type(request, pk):
    obj = get_object_or_404(Type, pk=pk)
    if request.method == 'POST':
        try:
            obj.delete()
            messages.success(request, f'Тип «{obj.name}» успешно удалён.')
        except IntegrityError:
            messages.error(
                request,
                f'Нельзя удалить тип «{obj.name}»: он используется в записях.'
            )
        return redirect('references')
    return redirect('references')


# --- Status ---

def add_status(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            Status.objects.create(name=name)
            messages.success(request, 'Статус успешно добавлен.')
    return redirect('references')


def delete_status(request, pk):
    obj = get_object_or_404(Status, pk=pk)
    if request.method == 'POST':
        try:
            obj.delete()
            messages.success(request, f'Статус «{obj.name}» успешно удалён.')
        except IntegrityError:
            messages.error(
                request,
                f'Нельзя удалить статус «{obj.name}»: он используется в записях.'
            )
        return redirect('references')
    return redirect('references')


# --- Category ---

def add_category(request):
    if request.method == 'POST':
        type_id = request.POST.get('type')
        name = request.POST.get('name', '').strip()
        if type_id and name:
            Category.objects.create(type_id=type_id, name=name)
            messages.success(request, 'Категория успешно добавлена.')
    return redirect('references')


def delete_category(request, pk):
    obj = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        try:
            obj.delete()
            messages.success(request, f'Категория «{obj.name}» успешно удалена.')
        except IntegrityError:
            messages.error(
                request,
                f'Нельзя удалить категорию «{obj.name}»: она используется в записях.'
            )
        return redirect('references')
    return redirect('references')


# --- Subcategory ---

def add_subcategory(request):
    if request.method == 'POST':
        category_id = request.POST.get('category')
        name = request.POST.get('name', '').strip()
        if category_id and name:
            Subcategory.objects.create(category_id=category_id, name=name)
            messages.success(request, 'Подкатегория успешно добавлена.')
    return redirect('references')


def delete_subcategory(request, pk):
    obj = get_object_or_404(Subcategory, pk=pk)
    if request.method == 'POST':
        try:
            obj.delete()
            messages.success(request, f'Подкатегория «{obj.name}» успешно удалена.')
        except IntegrityError:
            messages.error(
                request,
                f'Нельзя удалить подкатегорию «{obj.name}»: она используется в записях.'
            )
        return redirect('references')
    return redirect('references')


# --- Редактирование справочников ---

def edit_type(request, pk):
    obj = get_object_or_404(Type, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            obj.name = name
            obj.save()
            messages.success(request, 'Тип успешно обновлён.')
            return redirect('references')
    return render(request, 'core/reference_edit.html', {
        'object': obj,
        'title': 'Редактировать тип',
        'back_url': 'references'
    })


def edit_status(request, pk):
    obj = get_object_or_404(Status, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            obj.name = name
            obj.save()
            messages.success(request, 'Статус успешно обновлён.')
            return redirect('references')
    return render(request, 'core/reference_edit.html', {
        'object': obj,
        'title': 'Редактировать статус',
        'back_url': 'references'
    })


def edit_category(request, pk):
    obj = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        type_id = request.POST.get('type')
        if name and type_id:
            obj.name = name
            obj.type_id = type_id
            obj.save()
            messages.success(request, 'Категория успешно обновлена.')
            return redirect('references')
    context = {
        'object': obj,
        'title': 'Редактировать категорию',
        'types': Type.objects.all(),
        'back_url': 'references'
    }
    return render(request, 'core/reference_edit_category.html', context)


def edit_subcategory(request, pk):
    obj = get_object_or_404(Subcategory, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        category_id = request.POST.get('category')
        if name and category_id:
            obj.name = name
            obj.category_id = category_id
            obj.save()
            messages.success(request, 'Подкатегория успешно обновлена.')
            return redirect('references')
    context = {
        'object': obj,
        'title': 'Редактировать подкатегорию',
        'categories': Category.objects.select_related('type').all(),
        'back_url': 'references'
    }
    return render(request, 'core/reference_edit_subcategory.html', context)

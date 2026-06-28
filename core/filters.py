import django_filters
from django import forms
from .models import CashFlowRecord, Status, Type, Category, Subcategory

class CashFlowFilter(django_filters.FilterSet):
    date__gte = django_filters.DateFilter(
        field_name='date',
        lookup_expr='gte',
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата от'
    )
    date__lte = django_filters.DateFilter(
        field_name='date',
        lookup_expr='lte',
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата до'
    )

    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label='Статус'
    )
    type = django_filters.ModelChoiceFilter(
        queryset=Type.objects.all(),
        label='Тип операции'
    )
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        label='Категория'
    )
    subcategory = django_filters.ModelChoiceFilter(
        queryset=Subcategory.objects.all(),
        label='Подкатегория'
    )

    class Meta:
        model = CashFlowRecord
        fields = []
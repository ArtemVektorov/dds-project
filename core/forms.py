from django import forms
from .models import CashFlowRecord, Category, Subcategory


from django import forms
from .models import CashFlowRecord

class CashFlowForm(forms.ModelForm):
    class Meta:
        model = CashFlowRecord
        fields = ['date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment']
        labels = {
            'date': 'Дата',
            'status': 'Статус',
            'type': 'Тип операции',
            'category': 'Категория',
            'subcategory': 'Подкатегория',
            'amount': 'Сумма (₽)',
            'comment': 'Комментарий',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in ['amount', 'type', 'category', 'subcategory']:
            self.fields[field].required = True

        self.fields['type'].widget.attrs.update({'class': 'form-select'})
        self.fields['category'].widget.attrs.update({'class': 'form-select'})
        self.fields['subcategory'].widget.attrs.update({'class': 'form-select'})

        # === Ключевой момент ===
        if args:  # POST запрос
            type_id = args[0].get('type')
            category_id = args[0].get('category')

            if type_id:
                self.fields['category'].queryset = Category.objects.filter(type_id=type_id)
            if category_id:
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id)

        elif self.instance.pk:  # Редактирование (GET)
            self.fields['category'].queryset = Category.objects.filter(type=self.instance.type)
            self.fields['subcategory'].queryset = Subcategory.objects.filter(category=self.instance.category)
        else:  # Создание новой записи
            self.fields['category'].queryset = Category.objects.none()
            self.fields['subcategory'].queryset = Subcategory.objects.none()
            # Для JavaScript при редактировании
        if self.instance.pk:
            self.fields['category'].widget.attrs['data-initial'] = self.instance.category_id
            self.fields['subcategory'].widget.attrs['data-initial'] = self.instance.subcategory_id
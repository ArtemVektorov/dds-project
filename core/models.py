from django.db import models
from django.utils import timezone


class Type(models.Model):  # Пополнение / Списание
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=200)

    class Meta:
        unique_together = ('type', 'name')

    def __str__(self):
        return f"{self.name} ({self.type.name})"


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=200)

    class Meta:
        unique_together = ('category', 'name')

    def __str__(self):
        return self.name


class CashFlowRecord(models.Model):
    date = models.DateField(default=timezone.now)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    type = models.ForeignKey(Type, on_delete=models.PROTECT)    # Пополнение/Списание
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.date} | {self.type} | {self.amount} ₽"
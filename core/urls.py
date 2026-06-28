from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main'),

    # Записи
    path('record/create/', views.record_create, name='record_create'),
    path('record/<int:pk>/edit/', views.record_edit, name='record_edit'),
    path('record/<int:pk>/delete/', views.record_delete, name='record_delete'),

    # AJAX для зависимых списков
    path('load-categories/', views.load_categories, name='load_categories'),
    path('load-subcategories/', views.load_subcategories, name='load_subcategories'),

    # Справочники
    path('references/', views.references_page, name='references'),


    # type
    path('references/add-type/', views.add_type, name='add_type'),
    path('references/delete-type/<int:pk>/', views.delete_type, name='delete_type'),
    path('references/edit-type/<int:pk>/', views.edit_type, name='edit_type'),

    # status
    path('references/add-status/', views.add_status, name='add_status'),
    path('references/delete-status/<int:pk>/', views.delete_status, name='delete_status'),
    path('references/edit-status/<int:pk>/', views.edit_status, name='edit_status'),


    # category
    path('references/add-category/', views.add_category, name='add_category'),
    path('references/delete-category/<int:pk>/', views.delete_category, name='delete_category'),
    path('references/edit-category/<int:pk>/', views.edit_category, name='edit_category'),

    # subcategory
    path('references/add-subcategory/', views.add_subcategory, name='add_subcategory'),
    path('references/delete-subcategory/<int:pk>/', views.delete_subcategory, name='delete_subcategory'),
    path('references/edit-subcategory/<int:pk>/', views.edit_subcategory, name='edit_subcategory'),
]

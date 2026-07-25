from django.urls import path

from . import views

app_name = 'documents'

urlpatterns = [
    path('', views.documents_hub, name='hub'),
    path('dop/', views.dop_list, name='dop_list'),
    path('dop/create/', views.dop_create, name='dop_create'),
    path('dop/settings/', views.dop_settings, name='dop_settings'),
    path('dop/<int:pk>/edit/', views.dop_edit, name='dop_edit'),
    path('dop/<int:pk>/print/', views.dop_print, name='dop_print'),
    path('dop/<int:pk>/email/', views.dop_email, name='dop_email'),
    path('dop/<int:pk>/pdf/', views.dop_pdf, name='dop_pdf'),
    path('dop/<int:pk>/delete/', views.dop_delete, name='dop_delete'),
]
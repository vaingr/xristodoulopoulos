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
    path('en1279/', views.en1279_list, name='en1279_list'),
    path('en1279/create/', views.en1279_create, name='en1279_create'),
    path('en1279/settings/', views.en1279_settings, name='en1279_settings'),
    path('en1279/options/', views.en1279_options, name='en1279_options'),
    path('en1279/<int:pk>/edit/', views.en1279_edit, name='en1279_edit'),
    path('en1279/<int:pk>/print/', views.en1279_print, name='en1279_print'),
    path('en1279/<int:pk>/email/', views.en1279_email, name='en1279_email'),
    path('en1279/<int:pk>/pdf/', views.en1279_pdf, name='en1279_pdf'),
    path('en1279/<int:pk>/delete/', views.en1279_delete, name='en1279_delete'),
]

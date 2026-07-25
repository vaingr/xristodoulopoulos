from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.module_settings import get_module_flags

from .forms import DeclarationOfPerformanceForm, DopSettingsForm
from .models import (
    DOP_AUTHORIZED_REPRESENTATIVE,
    DOP_AVCP_SYSTEM,
    DOP_EUROPEAN_TECHNICAL_ASSESSMENT,
    DOP_HARMONISED_STANDARD,
    DOP_INTENDED_USE,
    DOP_MANUFACTURER,
    DeclarationOfPerformance,
    DopSettings,
)


def _documents_access_required(view_func):
    """Επιτρέπει πρόσβαση σε superusers ή όταν το module Έντυπα είναι ενεργό."""

    @login_required
    def _wrapped(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        if get_module_flags().get('documents', True):
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Δεν έχετε πρόσβαση στην ενότητα Έντυπα.')
        return redirect('dashboard')

    return _wrapped


def _dop_print_context(request, dop, pdf_mode=False):
    return {
        'dop': dop,
        'dop_settings': DopSettings.get_solo(),
        'pdf_mode': pdf_mode,
        'intended_use': DOP_INTENDED_USE,
        'manufacturer': DOP_MANUFACTURER,
        'authorized_representative': DOP_AUTHORIZED_REPRESENTATIVE,
        'avcp_system': DOP_AVCP_SYSTEM,
        'harmonised_standard': DOP_HARMONISED_STANDARD,
        'european_technical_assessment': DOP_EUROPEAN_TECHNICAL_ASSESSMENT,
    }


@_documents_access_required
def documents_hub(request):
    return render(request, 'documents/hub.html')


@_documents_access_required
def dop_list(request):
    documents = (
        DeclarationOfPerformance.objects
        .select_related('created_by')
        .order_by('-created_at')
    )
    search_query = request.GET.get('search', '').strip()
    if search_query:
        documents = documents.filter(
            Q(document_number__icontains=search_query)
            | Q(source_document_number__icontains=search_query)
            | Q(source_document_type__icontains=search_query)
        )

    return render(request, 'documents/dop_list.html', {
        'documents': documents,
        'search_query': search_query,
    })


@_documents_access_required
def dop_create(request):
    if request.method == 'POST':
        form = DeclarationOfPerformanceForm(request.POST)
        if form.is_valid():
            dop = form.save(commit=False)
            dop.created_by = request.user
            dop.save()
            messages.success(
                request,
                f'Η δήλωση απόδοσης δημιουργήθηκε για {dop.get_identification_line()}.',
            )
            return redirect('documents:dop_print', pk=dop.pk)
    else:
        form = DeclarationOfPerformanceForm()

    return render(request, 'documents/dop_form.html', {
        'form': form,
        'page_title': 'Νέα Δήλωση Απόδοσης',
        'is_edit': False,
    })


@_documents_access_required
def dop_edit(request, pk):
    dop = get_object_or_404(DeclarationOfPerformance, pk=pk)
    if request.method == 'POST':
        form = DeclarationOfPerformanceForm(request.POST, instance=dop)
        if form.is_valid():
            dop = form.save()
            messages.success(
                request,
                f'Η δήλωση απόδοσης ενημερώθηκε ({dop.get_identification_line()}).',
            )
            return redirect('documents:dop_print', pk=dop.pk)
    else:
        form = DeclarationOfPerformanceForm(instance=dop)

    return render(request, 'documents/dop_form.html', {
        'form': form,
        'page_title': f'Επεξεργασία Δηλώσης {dop.document_number}',
        'dop': dop,
        'is_edit': True,
    })


@_documents_access_required
def dop_delete(request, pk):
    dop = get_object_or_404(DeclarationOfPerformance, pk=pk)
    if request.method == 'POST':
        label = dop.get_identification_line()
        dop.delete()
        messages.success(request, f'Η δήλωση απόδοσης ({label}) διαγράφηκε.')
        return redirect('documents:dop_list')

    return render(request, 'documents/dop_confirm_delete.html', {
        'dop': dop,
    })


@_documents_access_required
def dop_settings(request):
    settings_obj = DopSettings.get_solo()
    if request.method == 'POST':
        form = DopSettingsForm(request.POST, request.FILES, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Οι ρυθμίσεις εντύπου αποθηκεύτηκαν επιτυχώς.')
            return redirect('documents:dop_settings')
    else:
        form = DopSettingsForm(instance=settings_obj)

    return render(request, 'documents/dop_settings.html', {
        'form': form,
        'settings': settings_obj,
    })


@_documents_access_required
def dop_print(request, pk):
    dop = get_object_or_404(
        DeclarationOfPerformance.objects.select_related('created_by'),
        pk=pk,
    )
    return render(
        request,
        'documents/dop_print.html',
        _dop_print_context(request, dop, pdf_mode=request.GET.get('pdf') == '1'),
    )

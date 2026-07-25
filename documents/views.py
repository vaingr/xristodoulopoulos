from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from accounts.module_settings import get_module_flags
from email_utils import get_email_settings, is_email_configured, send_email_with_attachment

from .forms import DeclarationOfPerformanceForm, DopEmailForm, DopSettingsForm
from .models import DeclarationOfPerformance, DopSettings
from .pdf_utils import generate_dop_pdf


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


def _dop_print_context(request, dop, pdf_mode=False, email_form=None):
    return {
        'dop': dop,
        'dop_settings': DopSettings.get_solo(),
        'pdf_mode': pdf_mode,
        'email_configured': is_email_configured(),
        'email_form': email_form or DopEmailForm(),
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
            dop.show_signature = bool(form.cleaned_data.get('show_signature'))
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
            dop = form.save(commit=False)
            dop.show_signature = bool(form.cleaned_data.get('show_signature'))
            dop.save()
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


@_documents_access_required
def dop_email(request, pk):
    dop = get_object_or_404(DeclarationOfPerformance, pk=pk)
    if request.method != 'POST':
        return redirect('documents:dop_print', pk=pk)

    email_form = DopEmailForm(request.POST)
    if not email_form.is_valid():
        for field_errors in email_form.errors.values():
            for error in field_errors:
                messages.error(request, error)
        return redirect('documents:dop_print', pk=pk)

    if not is_email_configured():
        messages.error(
            request,
            'Οι ρυθμίσεις email δεν έχουν ολοκληρωθεί. Ρυθμίστε τον SMTP server από τις ρυθμίσεις συστήματος.',
        )
        return redirect('documents:dop_print', pk=pk)

    recipient_email = email_form.cleaned_data['email'].strip()
    custom_message = email_form.cleaned_data.get('message', '').strip()

    email_settings = get_email_settings()
    sender_name = email_settings.get('from_name') or 'Χριστοδουλόπουλος'
    subject = f'{sender_name} - Δήλωση Απόδοσης {dop.document_number}'

    if custom_message:
        body = custom_message
    else:
        body = '\n'.join([
            f'Σας αποστέλλουμε συνημμένη τη δήλωση απόδοσης {dop.document_number}.',
            f'Παραστατικό: {dop.get_identification_line()}.',
            '',
            'Με εκτίμηση,',
        ])

    filename = f'dilosi-apodosis-{dop.document_number}.pdf'

    try:
        pdf_bytes = generate_dop_pdf(dop, request)
    except Exception as exc:
        messages.error(request, f'Αποτυχία δημιουργίας PDF: {exc}')
        return redirect('documents:dop_print', pk=pk)

    success, response_message = send_email_with_attachment(
        recipient_email,
        subject,
        body,
        pdf_bytes,
        filename,
    )

    if success:
        messages.success(request, f'Η δήλωση απόδοσης στάλθηκε στο email {recipient_email}.')
    else:
        messages.error(request, response_message or 'Αποτυχία αποστολής email.')

    return redirect('documents:dop_print', pk=pk)


@_documents_access_required
def dop_pdf(request, pk):
    dop = get_object_or_404(DeclarationOfPerformance, pk=pk)

    try:
        pdf_bytes = generate_dop_pdf(dop, request)
    except Exception as exc:
        messages.error(request, f'Αποτυχία δημιουργίας PDF: {exc}')
        return redirect('documents:dop_print', pk=pk)

    filename = f'dilosi-apodosis-{dop.document_number}.pdf'
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

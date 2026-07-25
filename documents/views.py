from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from accounts.module_settings import get_module_flags
from email_utils import get_email_settings, is_email_configured, send_email_with_attachment

from .forms import (
    DeclarationOfPerformanceForm,
    DopEmailForm,
    DopSettingsForm,
    En1279DocumentForm,
    En1279FieldOptionForm,
    En1279SettingsForm,
)
from .models import (
    DeclarationOfPerformance,
    DopSettings,
    En1279Document,
    En1279FieldOption,
    En1279Settings,
)
from .pdf_utils import generate_dop_pdf, generate_en1279_pdf


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
    if not request.user.is_superuser:
        messages.error(request, 'Μόνο οι superusers έχουν πρόσβαση στις ρυθμίσεις εντύπου.')
        return redirect('documents:dop_list')

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


def _en1279_print_context(request, doc, pdf_mode=False, email_form=None):
    en_settings = En1279Settings.get_solo()
    return {
        'doc': doc,
        'en_settings': en_settings,
        'table_rows': en_settings.get_table_rows(doc),
        'pdf_mode': pdf_mode,
        'email_configured': is_email_configured(),
        'email_form': email_form or DopEmailForm(),
    }


@_documents_access_required
def en1279_settings(request):
    if not request.user.is_superuser:
        messages.error(request, 'Μόνο οι superusers έχουν πρόσβαση στις ρυθμίσεις εντύπου.')
        return redirect('documents:en1279_list')

    settings_obj = En1279Settings.get_solo()
    if request.method == 'POST':
        form = En1279SettingsForm(request.POST, request.FILES, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Οι ρυθμίσεις εντύπου EN 1279-5 αποθηκεύτηκαν επιτυχώς.')
            return redirect('documents:en1279_settings')
    else:
        form = En1279SettingsForm(instance=settings_obj)

    row_forms = []
    for n in range(1, 14):
        row = {
            'num': n,
            'characteristic': form[f'row_{n}_characteristic'],
            'spec': form[f'row_{n}_spec'],
            'units': form[f'row_{n}_units'],
            'performance': form[f'row_{n}_performance'] if n <= 10 else None,
            'is_input_row': n >= 11,
        }
        row_forms.append(row)

    return render(request, 'documents/en1279_settings.html', {
        'form': form,
        'settings': settings_obj,
        'row_forms': row_forms,
    })


@_documents_access_required
def en1279_options(request):
    if request.method == 'POST':
        action = request.POST.get('action', 'add')
        if action == 'delete':
            option_id = request.POST.get('option_id')
            option = get_object_or_404(En1279FieldOption, pk=option_id)
            label = option.value
            option.delete()
            messages.success(request, f'Η επιλογή «{label}» διαγράφηκε.')
            return redirect('documents:en1279_options')

        form = En1279FieldOptionForm(request.POST)
        if form.is_valid():
            option = form.save(commit=False)
            option.value = option.value.strip()
            option.save()
            messages.success(
                request,
                f'Προστέθηκε επιλογή στο πεδίο «{option.get_field_key_display()}».',
            )
            return redirect('documents:en1279_options')
        messages.error(request, 'Δεν ήταν δυνατή η αποθήκευση της επιλογής. Έλεγξε τα πεδία.')
    else:
        form = En1279FieldOptionForm()

    option_groups = []
    for field_key, field_label in En1279FieldOption.FIELD_CHOICES:
        option_groups.append({
            'key': field_key,
            'label': field_label,
            'options': En1279FieldOption.objects.filter(field_key=field_key).order_by(
                'sort_order', 'value'
            ),
        })

    return render(request, 'documents/en1279_options.html', {
        'form': form,
        'option_groups': option_groups,
    })


@_documents_access_required
def en1279_list(request):
    documents = (
        En1279Document.objects
        .select_related('created_by')
        .order_by('-created_at')
    )
    search_query = request.GET.get('search', '').strip()
    if search_query:
        documents = documents.filter(
            Q(document_number__icontains=search_query)
            | Q(product_designation__icontains=search_query)
            | Q(thermal_performance__icontains=search_query)
            | Q(light_performance__icontains=search_query)
            | Q(energy_performance__icontains=search_query)
        )

    return render(request, 'documents/en1279_list.html', {
        'documents': documents,
        'search_query': search_query,
    })


@_documents_access_required
def en1279_create(request):
    if request.method == 'POST':
        form = En1279DocumentForm(request.POST)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.created_by = request.user
            doc.show_signature = bool(form.cleaned_data.get('show_signature'))
            doc.save()
            messages.success(
                request,
                f'Το έντυπο EN 1279-5 δημιουργήθηκε ({doc.document_number}).',
            )
            return redirect('documents:en1279_print', pk=doc.pk)
    else:
        form = En1279DocumentForm()

    return render(request, 'documents/en1279_form.html', {
        'form': form,
        'page_title': 'Νέο Έντυπο EN 1279-5',
        'is_edit': False,
    })


@_documents_access_required
def en1279_edit(request, pk):
    doc = get_object_or_404(En1279Document, pk=pk)
    if request.method == 'POST':
        form = En1279DocumentForm(request.POST, instance=doc)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.show_signature = bool(form.cleaned_data.get('show_signature'))
            doc.save()
            messages.success(
                request,
                f'Το έντυπο EN 1279-5 ενημερώθηκε ({doc.document_number}).',
            )
            return redirect('documents:en1279_print', pk=doc.pk)
    else:
        form = En1279DocumentForm(instance=doc)

    return render(request, 'documents/en1279_form.html', {
        'form': form,
        'page_title': f'Επεξεργασία EN 1279-5 {doc.document_number}',
        'doc': doc,
        'is_edit': True,
    })


@_documents_access_required
def en1279_delete(request, pk):
    doc = get_object_or_404(En1279Document, pk=pk)
    if request.method == 'POST':
        label = doc.document_number
        doc.delete()
        messages.success(request, f'Το έντυπο EN 1279-5 ({label}) διαγράφηκε.')
        return redirect('documents:en1279_list')

    return render(request, 'documents/en1279_confirm_delete.html', {
        'doc': doc,
    })


@_documents_access_required
def en1279_print(request, pk):
    doc = get_object_or_404(
        En1279Document.objects.select_related('created_by'),
        pk=pk,
    )
    return render(
        request,
        'documents/en1279_print.html',
        _en1279_print_context(request, doc, pdf_mode=request.GET.get('pdf') == '1'),
    )


@_documents_access_required
def en1279_email(request, pk):
    doc = get_object_or_404(En1279Document, pk=pk)
    if request.method != 'POST':
        return redirect('documents:en1279_print', pk=pk)

    email_form = DopEmailForm(request.POST)
    if not email_form.is_valid():
        for field_errors in email_form.errors.values():
            for error in field_errors:
                messages.error(request, error)
        return redirect('documents:en1279_print', pk=pk)

    if not is_email_configured():
        messages.error(
            request,
            'Οι ρυθμίσεις email δεν έχουν ολοκληρωθεί. Ρυθμίστε τον SMTP server από τις ρυθμίσεις συστήματος.',
        )
        return redirect('documents:en1279_print', pk=pk)

    recipient_email = email_form.cleaned_data['email'].strip()
    custom_message = email_form.cleaned_data.get('message', '').strip()

    email_settings = get_email_settings()
    sender_name = email_settings.get('from_name') or 'Χριστοδουλόπουλος'
    subject = f'{sender_name} - Έντυπο EN 1279-5 {doc.document_number}'

    if custom_message:
        body = custom_message
    else:
        body = '\n'.join([
            f'Σας αποστέλλουμε συνημμένο το έντυπο EN 1279-5 {doc.document_number}.',
            f'Τύπος προϊόντος: {doc.product_designation}.',
            '',
            'Με εκτίμηση,',
        ])

    filename = f'en1279-5-{doc.document_number}.pdf'

    try:
        pdf_bytes = generate_en1279_pdf(doc, request)
    except Exception as exc:
        messages.error(request, f'Αποτυχία δημιουργίας PDF: {exc}')
        return redirect('documents:en1279_print', pk=pk)

    success, response_message = send_email_with_attachment(
        recipient_email,
        subject,
        body,
        pdf_bytes,
        filename,
    )

    if success:
        messages.success(request, f'Το έντυπο EN 1279-5 στάλθηκε στο email {recipient_email}.')
    else:
        messages.error(request, response_message or 'Αποτυχία αποστολής email.')

    return redirect('documents:en1279_print', pk=pk)


@_documents_access_required
def en1279_pdf(request, pk):
    doc = get_object_or_404(En1279Document, pk=pk)

    try:
        pdf_bytes = generate_en1279_pdf(doc, request)
    except Exception as exc:
        messages.error(request, f'Αποτυχία δημιουργίας PDF: {exc}')
        return redirect('documents:en1279_print', pk=pk)

    filename = f'en1279-5-{doc.document_number}.pdf'
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

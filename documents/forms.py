from django import forms

from .models import DeclarationOfPerformance, DopSettings, En1279Document, En1279Settings


class ShowSignatureCheckboxInput(forms.CheckboxInput):
    def value_from_datadict(self, data, files, name):
        # Με hidden false + checkbox true, το QueryDict μπορεί να έχει και τα δύο.
        # Παίρνουμε την τελευταία τιμή (του checkbox αν είναι τσεκαρισμένο).
        if hasattr(data, 'getlist'):
            values = data.getlist(name)
            if values:
                raw = values[-1]
            else:
                raw = None
        else:
            raw = data.get(name)

        if raw is None:
            return False
        if isinstance(raw, str):
            return raw.lower() in ('true', '1', 'on', 'yes')
        return bool(raw)


class DeclarationOfPerformanceForm(forms.ModelForm):
    class Meta:
        model = DeclarationOfPerformance
        fields = [
            'source_document_type',
            'source_document_number',
            'show_signature',
        ]
        widgets = {
            'source_document_type': forms.Select(attrs={'class': 'form-control'}),
            'source_document_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'π.χ. 1260',
                'autocomplete': 'off',
            }),
            'show_signature': ShowSignatureCheckboxInput(attrs={
                'class': 'dop-checkbox',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['source_document_type'].label = 'Τύπος παραστατικού'
        self.fields['source_document_number'].label = 'Αριθμός παραστατικού'
        self.fields['show_signature'].label = 'Εμφάνιση Υπογραφής'
        self.fields['source_document_type'].choices = [
            choice for choice in DeclarationOfPerformance.SOURCE_CHOICES
        ]
        if not self.instance.pk and 'show_signature' not in self.initial:
            self.fields['show_signature'].initial = True


class DopEmailForm(forms.Form):
    email = forms.EmailField(
        label='Email παραλήπτη',
        widget=forms.EmailInput(attrs={
            'class': 'dop-email-input',
            'id': 'id_dop_email',
            'placeholder': 'π.χ. customer@example.com',
            'autocomplete': 'email',
        }),
    )
    message = forms.CharField(
        required=False,
        label='Μήνυμα',
        widget=forms.Textarea(attrs={
            'class': 'dop-email-message',
            'id': 'id_dop_email_message',
            'rows': 4,
            'placeholder': 'Προαιρετικό μήνυμα στο email...',
        }),
    )


class En1279DocumentForm(forms.ModelForm):
    class Meta:
        model = En1279Document
        fields = [
            'product_designation',
            'thermal_performance',
            'light_performance',
            'energy_performance',
            'show_signature',
        ]
        widgets = {
            'product_designation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'π.χ. 4mm PLANISTAR 60 - 16mm (argon 90%) - 4mm CLEAR',
                'autocomplete': 'off',
            }),
            'thermal_performance': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'π.χ. 1,0',
                'autocomplete': 'off',
            }),
            'light_performance': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'π.χ. 61% - 23%',
                'autocomplete': 'off',
            }),
            'energy_performance': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'π.χ. 0,38 - 38%',
                'autocomplete': 'off',
            }),
            'show_signature': ShowSignatureCheckboxInput(attrs={
                'class': 'dop-checkbox',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_designation'].label = 'Τύπος προϊόντος / Designation of product'
        self.fields['thermal_performance'].label = 'Συντελεστής θερμοαγωγιμότητας U (γραμμή 11)'
        self.fields['light_performance'].label = 'Μετάδοση φωτός - αντανάκλαση φωτός (γραμμή 12)'
        self.fields['energy_performance'].label = 'Ηλιακός συντελεστής / Αντανάκλαση ενέργειας (γραμμή 13)'
        self.fields['show_signature'].label = 'Εμφάνιση Υπογραφής'
        if not self.instance.pk and 'show_signature' not in self.initial:
            self.fields['show_signature'].initial = True


class GreekClearableFileInput(forms.ClearableFileInput):
    template_name = 'documents/widgets/clearable_file_input.html'
    initial_text = 'Τρέχον αρχείο'
    input_text = 'Αλλαγή αρχείου'
    clear_checkbox_label = 'Διαγραφή τρέχοντος'


_SECTION_FIELDS = []
for _n in range(1, 9):
    _SECTION_FIELDS.append(f'section_{_n}_label')
    if _n != 1:
        _SECTION_FIELDS.append(f'section_{_n}_value')


class DopSettingsForm(forms.ModelForm):
    class Meta:
        model = DopSettings
        fields = [
            'logo',
            'logo_as_watermark',
            'signature',
            'ce_mark',
            'header_company_name',
            'header_company_activity',
            'header_company_details',
            *_SECTION_FIELDS,
        ]
        labels = {
            'logo': 'Λογότυπο',
            'logo_as_watermark': 'Υδατογράφημα',
            'signature': 'Υπογραφή',
            'ce_mark': 'Σήμανση CE',
            'header_company_name': 'Επωνυμία',
            'header_company_activity': 'Δραστηριότητα',
            'header_company_details': 'Στοιχεία επικοινωνίας',
            'section_1_label': 'Τίτλος',
            'section_2_label': 'Τίτλος',
            'section_2_value': 'Κείμενο',
            'section_3_label': 'Τίτλος',
            'section_3_value': 'Κείμενο',
            'section_4_label': 'Τίτλος',
            'section_4_value': 'Κείμενο',
            'section_5_label': 'Τίτλος',
            'section_5_value': 'Κείμενο',
            'section_6_label': 'Τίτλος',
            'section_6_value': 'Κείμενο',
            'section_7_label': 'Τίτλος',
            'section_7_value': 'Κείμενο',
            'section_8_label': 'Τίτλος',
            'section_8_value': 'Κείμενο',
        }
        widgets = {
            'logo': GreekClearableFileInput(attrs={
                'class': 'dop-file-input',
                'accept': 'image/*',
            }),
            'logo_as_watermark': forms.CheckboxInput(attrs={
                'class': 'dop-watermark-checkbox',
            }),
            'signature': GreekClearableFileInput(attrs={
                'class': 'dop-file-input',
                'accept': 'image/*',
            }),
            'ce_mark': GreekClearableFileInput(attrs={
                'class': 'dop-file-input',
                'accept': 'image/*',
            }),
            'header_company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
            }),
            'header_company_activity': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
            }),
            'header_company_details': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
            }),
            **{
                f'section_{n}_label': forms.Textarea(attrs={
                    'class': 'form-control',
                    'rows': 3,
                })
                for n in range(1, 9)
            },
            **{
                f'section_{n}_value': forms.Textarea(attrs={
                    'class': 'form-control',
                    'rows': 2,
                })
                for n in range(2, 9)
            },
        }

    def _clean_image(self, field_name, label):
        image = self.cleaned_data.get(field_name)
        if not image or not hasattr(image, 'content_type'):
            return image

        if image.size > 2 * 1024 * 1024:
            raise forms.ValidationError(f'Το {label} δεν μπορεί να υπερβαίνει το 2 MB.')

        content_type = getattr(image, 'content_type', '')
        if content_type and not content_type.startswith('image/'):
            raise forms.ValidationError('Επιτρέπονται μόνο αρχεία εικόνας.')

        return image

    def clean_logo(self):
        return self._clean_image('logo', 'λογότυπο')

    def clean_signature(self):
        return self._clean_image('signature', 'αρχείο υπογραφής')

    def clean_ce_mark(self):
        return self._clean_image('ce_mark', 'αρχείο σήμανσης CE')


class En1279SettingsForm(forms.ModelForm):
    class Meta:
        model = En1279Settings
        fields = [
            'logo',
            'logo_as_watermark',
            'signature',
            'ce_mark',
            'header_company_name',
            'header_company_activity',
            'header_company_details',
            'standard_intro',
            'standard_code',
            'product_name_label',
            'product_name_value',
            'designation_label',
            'col_characteristic',
            'col_spec',
            'col_units',
            'col_performance',
            'npd_note',
            *[
                field
                for n in range(1, 14)
                for field in (
                    [f'row_{n}_characteristic', f'row_{n}_spec', f'row_{n}_units']
                    + ([f'row_{n}_performance'] if n <= 10 else [])
                )
            ],
        ]
        labels = {
            'logo': 'Λογότυπο',
            'logo_as_watermark': 'Υδατογράφημα',
            'signature': 'Υπογραφή',
            'ce_mark': 'Σήμανση CE',
            'header_company_name': 'Επωνυμία',
            'header_company_activity': 'Δραστηριότητα',
            'header_company_details': 'Στοιχεία επικοινωνίας',
            'standard_intro': 'Κείμενο προτύπου',
            'standard_code': 'Κωδικός προτύπου',
            'product_name_label': 'Τίτλος',
            'product_name_value': 'Κείμενο',
            'designation_label': 'Τίτλος τύπου προϊόντος',
            'col_characteristic': 'Στήλη ιδιότητας',
            'col_spec': 'Στήλη προδιαγραφής',
            'col_units': 'Στήλη μονάδων',
            'col_performance': 'Στήλη απόδοσης',
            'npd_note': 'Σημείωση NPD',
            **{
                f'row_{n}_characteristic': 'Ιδιότητα'
                for n in range(1, 14)
            },
            **{
                f'row_{n}_spec': 'Προδιαγραφή'
                for n in range(1, 14)
            },
            **{
                f'row_{n}_units': 'Μονάδες'
                for n in range(1, 14)
            },
            **{
                f'row_{n}_performance': 'Απόδοση'
                for n in range(1, 11)
            },
        }
        widgets = {
            'logo': GreekClearableFileInput(attrs={
                'class': 'dop-file-input',
                'accept': 'image/*',
            }),
            'logo_as_watermark': forms.CheckboxInput(attrs={
                'class': 'dop-watermark-checkbox',
            }),
            'signature': GreekClearableFileInput(attrs={
                'class': 'dop-file-input',
                'accept': 'image/*',
            }),
            'ce_mark': GreekClearableFileInput(attrs={
                'class': 'dop-file-input',
                'accept': 'image/*',
            }),
            'header_company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
            }),
            'header_company_activity': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
            }),
            'header_company_details': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
            }),
            'standard_intro': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
            }),
            'standard_code': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
            }),
            'product_name_label': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
            }),
            'product_name_value': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
            'designation_label': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
            }),
            'col_characteristic': forms.TextInput(attrs={'class': 'form-control'}),
            'col_spec': forms.TextInput(attrs={'class': 'form-control'}),
            'col_units': forms.TextInput(attrs={'class': 'form-control'}),
            'col_performance': forms.TextInput(attrs={'class': 'form-control'}),
            'npd_note': forms.TextInput(attrs={'class': 'form-control'}),
            **{
                f'row_{n}_characteristic': forms.Textarea(attrs={
                    'class': 'form-control',
                    'rows': 2,
                })
                for n in range(1, 14)
            },
            **{
                f'row_{n}_spec': forms.TextInput(attrs={'class': 'form-control'})
                for n in range(1, 14)
            },
            **{
                f'row_{n}_units': forms.TextInput(attrs={'class': 'form-control'})
                for n in range(1, 14)
            },
            **{
                f'row_{n}_performance': forms.TextInput(attrs={'class': 'form-control'})
                for n in range(1, 11)
            },
        }

    def _clean_image(self, field_name, label):
        image = self.cleaned_data.get(field_name)
        if not image or not hasattr(image, 'content_type'):
            return image

        if image.size > 2 * 1024 * 1024:
            raise forms.ValidationError(f'Το {label} δεν μπορεί να υπερβαίνει το 2 MB.')

        content_type = getattr(image, 'content_type', '')
        if content_type and not content_type.startswith('image/'):
            raise forms.ValidationError('Επιτρέπονται μόνο αρχεία εικόνας.')

        return image

    def clean_logo(self):
        return self._clean_image('logo', 'λογότυπο')

    def clean_signature(self):
        return self._clean_image('signature', 'αρχείο υπογραφής')

    def clean_ce_mark(self):
        return self._clean_image('ce_mark', 'αρχείο σήμανσης CE')

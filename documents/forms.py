from django import forms

from .models import DeclarationOfPerformance, DopSettings


class DeclarationOfPerformanceForm(forms.ModelForm):
    class Meta:
        model = DeclarationOfPerformance
        fields = [
            'source_document_type',
            'source_document_number',
        ]
        widgets = {
            'source_document_type': forms.Select(attrs={'class': 'form-control'}),
            'source_document_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'π.χ. 1260',
                'autocomplete': 'off',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['source_document_type'].label = 'Τύπος παραστατικού'
        self.fields['source_document_number'].label = 'Αριθμός παραστατικού'
        self.fields['source_document_type'].choices = [
            choice for choice in DeclarationOfPerformance.SOURCE_CHOICES
        ]


class GreekClearableFileInput(forms.ClearableFileInput):
    template_name = 'documents/widgets/clearable_file_input.html'
    initial_text = 'Τρέχον αρχείο'
    input_text = 'Αλλαγή αρχείου'
    clear_checkbox_label = 'Διαγραφή τρέχοντος'


class DopSettingsForm(forms.ModelForm):
    class Meta:
        model = DopSettings
        fields = ['logo', 'logo_as_watermark', 'signature']
        labels = {
            'logo': 'Λογότυπο',
            'logo_as_watermark': 'Υδατογράφημα',
            'signature': 'Υπογραφή',
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

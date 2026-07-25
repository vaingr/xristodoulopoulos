from django.conf import settings
from django.db import models
from django.utils import timezone


# Σταθερά κείμενα εντύπου (όπως στο έντυπο της εταιρείας)
DOP_INTENDED_USE = (
    'Διπλοί μονωτικοί υαλοπίνακες που πρόκειται να χρησιμοποιηθούν '
    'σε κτήρια και κατασκευαστικά έργα'
)
DOP_MANUFACTURER = 'ΧΡΙΣΤΟΔΟΥΛΟΠΟΥΛΟΣ Γ. ΑΝΑΣΤΑΣΙΟΣ, ΕΛ. ΒΕΝΙΖΕΛΟΥ 40, ΑΜΑΛΙΑΔΑ'
DOP_AUTHORIZED_REPRESENTATIVE = 'Δεν εφαρμόζεται'
DOP_AVCP_SYSTEM = 'Σύστημα 3'
DOP_HARMONISED_STANDARD = (
    'Βάσει του προτύπου EN 1279-5:2010, με σύμβαση sharing 22/2/2018'
)
DOP_EUROPEAN_TECHNICAL_ASSESSMENT = 'Δεν εφαρμόζεται'


class DopSettings(models.Model):
    """Ρυθμίσεις εντύπου Δηλώσης Απόδοσης (singleton)."""

    logo = models.ImageField(
        upload_to='documents/dop/logo/',
        blank=True,
        null=True,
        verbose_name='Λογότυπο',
    )
    logo_as_watermark = models.BooleanField(
        default=False,
        verbose_name='Υδατογράφημα',
    )
    signature = models.ImageField(
        upload_to='documents/dop/signature/',
        blank=True,
        null=True,
        verbose_name='Υπογραφή',
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Τελευταία ενημέρωση')

    class Meta:
        verbose_name = 'Ρυθμίσεις Δηλώσης Απόδοσης'
        verbose_name_plural = 'Ρυθμίσεις Δηλώσης Απόδοσης'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return 'Ρυθμίσεις Δηλώσης Απόδοσης'


class DeclarationOfPerformance(models.Model):
    """Δήλωση Απόδοσης (DoP) για εκτύπωση."""

    SOURCE_INVOICE_DELIVERY = 'invoice_delivery'
    SOURCE_RETAIL = 'retail'
    SOURCE_CHOICES = [
        (SOURCE_INVOICE_DELIVERY, 'ΤΙΜΟΛΟΓΙΟ - ΔΕΛΤΙΟ ΑΠΟΣΤΟΛΗΣ'),
        (SOURCE_RETAIL, 'ΑΠΟΔΕΙΞΗ ΛΙΑΝΙΚΗΣ'),
    ]

    document_number = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='Αριθμός Δηλώσης',
    )
    source_document_type = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        verbose_name='Τύπος παραστατικού',
    )
    source_document_number = models.CharField(
        max_length=50,
        verbose_name='Αριθμός παραστατικού',
    )
    product = models.ForeignKey(
        'products.FinishedProduct',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='declarations_of_performance',
        verbose_name='Προϊόν',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ημερομηνία Δημιουργίας')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='dops_created',
        verbose_name='Δημιουργήθηκε από',
    )

    class Meta:
        verbose_name = 'Δήλωση Απόδοσης'
        verbose_name_plural = 'Δηλώσεις Απόδοσης'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.document_number} - {self.get_source_label()}'

    def get_source_label(self):
        return self.get_source_document_type_display()

    def get_identification_line(self):
        return (
            f'{self.get_source_document_type_display()} '
            f'No {self.source_document_number}'
        )

    def save(self, *args, **kwargs):
        if not self.document_number:
            today = timezone.localdate()
            year_suffix = today.strftime('%y')
            suffix = f'-{year_suffix}'

            max_number = 0
            for document_number in DeclarationOfPerformance.objects.filter(
                document_number__endswith=suffix,
            ).values_list('document_number', flat=True):
                try:
                    sequence = int(document_number.split('-', 1)[0])
                except (ValueError, IndexError):
                    continue
                max_number = max(max_number, sequence)

            self.document_number = f'{max_number + 1:04d}{suffix}'
        super().save(*args, **kwargs)

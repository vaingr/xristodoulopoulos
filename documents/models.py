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

DOP_DEFAULT_HEADER_NAME = 'ΧΡΙΣΤΟΔΟΥΛΟΠΟΥΛΟΣ Γ. ΑΝΑΣΤΑΣΙΟΣ'
DOP_DEFAULT_HEADER_ACTIVITY = 'ΕΠΕΞΕΡΓΑΣΙΑ - ΕΜΠΟΡΙΑ ΥΑΛΟΠΙΝΑΚΩΝ'
DOP_DEFAULT_HEADER_DETAILS = (
    'Ελ. Βενιζέλου 40, Αμαλιάδα\n'
    'Τηλ. 26220 28686 · Κιν. 6977 240040\n'
    'Email: info@tasosxristodoulopoulosglass.gr\n'
    'ΑΦΜ: 043758710 · ΔΟΥ: Αμαλιάδας'
)

DOP_DEFAULT_SECTION_1_LABEL = '1. Μοναδικός κωδικός ταυτοποίησης προϊόντος'
DOP_DEFAULT_SECTION_2_LABEL = (
    '2. Αριθμός τύπου, παρτίδας ή σειράς ή οποιοδήποτε άλλο στοιχείο επιτρέπει την ταυτοποίηση '
    'του προϊόντος του τομέα των δομικών κατασκευών, όπως προβλέπει'
)
DOP_DEFAULT_SECTION_3_LABEL = (
    '3. Προτεινόμενη χρήση ή χρήσεις του προϊόντος του τομέα δομικών κατασκευών, σύμφωνα με την '
    'ισχύουσα εναρμονισμένη τεχνική προδιαγραφή, όπως προβλέπεται από τον κατασκευαστή:'
)
DOP_DEFAULT_SECTION_4_LABEL = (
    '4. Όνομα, εμπορική επωνυμία ή κατατεθέν σήμα και διεύθυνση επικοινωνίας του κατασκευαστή, '
    'όπως προβλέπεται στο άρθρο 11, παράγραφος 5:'
)
DOP_DEFAULT_SECTION_5_LABEL = (
    '5. Όπου εφαρμόζεται, όνομα και διεύθυνση επικοινωνίας του εξουσιοδοτημένου αντιπροσώπου, '
    'η εντολή του οποίου καλύπτει τα καθήκοντα που προβλέπονται στο άρθρο 12 παρ. 2:'
)
DOP_DEFAULT_SECTION_6_LABEL = (
    '6. Σύστημα ή συστήματα αξιολόγησης και επαλήθευσης της σταθερότητας της απόδοσης του προϊόντος '
    'του τομέα των δομικών κατασκευών όπως καθορίζεται στο παράρτημα V:'
)
DOP_DEFAULT_SECTION_7_LABEL = (
    '7. Σε περίπτωση δήλωσης απόδοσης σχετικά με προϊόν του τομέα δομικών κατασκευών που καλύπτεται '
    'από εναρμονισμένο πρότυπο:'
)
DOP_DEFAULT_SECTION_8_LABEL = (
    '8. Σε περίπτωση δήλωσης απόδοσης σχετικά με προϊόν του τομέα δομικών κατασκευών για το οποίο '
    'έχει εκδοθεί ευρωπαϊκή τεχνική αξιολόγηση:'
)


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
    ce_mark = models.ImageField(
        upload_to='documents/dop/ce/',
        blank=True,
        null=True,
        verbose_name='Σήμανση CE',
    )
    header_company_name = models.CharField(
        max_length=200,
        default=DOP_DEFAULT_HEADER_NAME,
        verbose_name='Επωνυμία κεφαλίδας',
    )
    header_company_activity = models.CharField(
        max_length=200,
        default=DOP_DEFAULT_HEADER_ACTIVITY,
        verbose_name='Δραστηριότητα κεφαλίδας',
    )
    header_company_details = models.TextField(
        default=DOP_DEFAULT_HEADER_DETAILS,
        verbose_name='Στοιχεία κεφαλίδας',
    )

    section_1_label = models.TextField(
        default=DOP_DEFAULT_SECTION_1_LABEL,
        verbose_name='Ενότητα 1 - Τίτλος',
    )
    section_2_label = models.TextField(
        default=DOP_DEFAULT_SECTION_2_LABEL,
        verbose_name='Ενότητα 2 - Τίτλος',
    )
    section_2_value = models.TextField(
        blank=True,
        default='',
        verbose_name='Ενότητα 2 - Κείμενο',
    )
    section_3_label = models.TextField(
        default=DOP_DEFAULT_SECTION_3_LABEL,
        verbose_name='Ενότητα 3 - Τίτλος',
    )
    section_3_value = models.TextField(
        default=DOP_INTENDED_USE,
        verbose_name='Ενότητα 3 - Κείμενο',
    )
    section_4_label = models.TextField(
        default=DOP_DEFAULT_SECTION_4_LABEL,
        verbose_name='Ενότητα 4 - Τίτλος',
    )
    section_4_value = models.TextField(
        default=DOP_MANUFACTURER,
        verbose_name='Ενότητα 4 - Κείμενο',
    )
    section_5_label = models.TextField(
        default=DOP_DEFAULT_SECTION_5_LABEL,
        verbose_name='Ενότητα 5 - Τίτλος',
    )
    section_5_value = models.TextField(
        default=DOP_AUTHORIZED_REPRESENTATIVE,
        verbose_name='Ενότητα 5 - Κείμενο',
    )
    section_6_label = models.TextField(
        default=DOP_DEFAULT_SECTION_6_LABEL,
        verbose_name='Ενότητα 6 - Τίτλος',
    )
    section_6_value = models.TextField(
        default=DOP_AVCP_SYSTEM,
        verbose_name='Ενότητα 6 - Κείμενο',
    )
    section_7_label = models.TextField(
        default=DOP_DEFAULT_SECTION_7_LABEL,
        verbose_name='Ενότητα 7 - Τίτλος',
    )
    section_7_value = models.TextField(
        default=DOP_HARMONISED_STANDARD,
        verbose_name='Ενότητα 7 - Κείμενο',
    )
    section_8_label = models.TextField(
        default=DOP_DEFAULT_SECTION_8_LABEL,
        verbose_name='Ενότητα 8 - Τίτλος',
    )
    section_8_value = models.TextField(
        default=DOP_EUROPEAN_TECHNICAL_ASSESSMENT,
        verbose_name='Ενότητα 8 - Κείμενο',
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
    show_signature = models.BooleanField(
        default=True,
        verbose_name='Εμφάνιση Υπογραφής',
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

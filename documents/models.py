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

EN1279_DEFAULT_STANDARD_INTRO = (
    'Σύμφωνα με τις απαιτήσεις του προτύπου / Under requirements of standart:'
)
EN1279_DEFAULT_STANDARD_CODE = 'EN 1279-5'
EN1279_DEFAULT_PRODUCT_NAME_LABEL = 'Περιγραφή του προϊόντος / Product name:'
EN1279_DEFAULT_PRODUCT_NAME_VALUE = (
    'Διπλοί μονωτικοί υαλοπίνακες που πρόκειται να χρησιμοποιηθούν σε κτίρια και κατασκευαστικά έργα / '
    'insulating glass unit, intended to be used in buildings and building works.'
)
EN1279_DEFAULT_DESIGNATION_LABEL = 'Τύπος προϊόντος: / Designation of product:'
EN1279_DEFAULT_COL_CHARACTERISTIC = 'ΙΔΙΟΤΗΤΑ / CHARACTERISTIC'
EN1279_DEFAULT_COL_SPEC = 'ΕΝΑΡΜΟΝΙΣΜΕΝΗ ΤΕΧΝΙΚΗ ΠΡΟΔΙΑΓΡΑΦΗ'
EN1279_DEFAULT_COL_UNITS = 'ΜΟΝΑΔΕΣ'
EN1279_DEFAULT_COL_PERFORMANCE = 'ΑΠΟΔΟΣΗ / PERFORMANCE'
EN1279_DEFAULT_NPD_NOTE = 'NPD-No performance determined'

# (characteristic, spec, units, performance) — performance editable for rows 1–10
EN1279_ROW_DEFAULTS = (
    ('Αντίσταση στην φωτιά / Resistance to fire', 'EN-13501-2', 'Κλάση', 'npd'),
    ('Αντίδραση στην φωτιά / Reaction to fire', 'EN-13501-1', 'Κλάση', 'npd'),
    ('Αντίσταση σε εξωτερική φωτιά / Behaviour of external fire', 'EN 1279-5', 'Κλάση', 'npd'),
    ('Αντίσταση σε σφαίρα / Bullet resistance', 'EN 1063', 'Κλάση', 'npd'),
    ('Αντίσταση σε έκρηξη / Resistance to explosion', 'EN 13541', 'Κλάση', 'npd'),
    ('Αντίσταση σε διάρρηξη / Resistance to hand attack', 'EN 356', 'Κλάση', 'npd'),
    (
        'Αντίσταση σε κρούση εκκρεμών αντικειμένων / Resistance to pendulum impact',
        'EN 12600',
        'Κλάση',
        'npd',
    ),
    (
        'Αντίσταση κατά ξαφνικών αλλαγών θερμοκρασίας και ανισοκατανομής θερμοκρασίας / '
        'Resistance to temperature differentials and temperature gradient',
        'EN 572',
        '[°K]',
        'npd',
    ),
    (
        'Μόνιμη επιβαλλόμενη ανεμοπίεση, χιόνι, μόνιμα και/ή επιβαλλόμενα φορτία / '
        'Resistance to wind, snow, permanent and/or imposed load',
        'EN 1279-5',
        'mm',
        'npd',
    ),
    (
        'Μόνωση κατά απευθείας αερομεταφερόμενου θορύβου / Direct airborne sound reduction',
        'EN 12758',
        'dB',
        'npd',
    ),
    (
        'Θερμικές ιδιότητες. Συντελεστής θερμοαγωγιμότητας / Thermal transmittance factor',
        'EN 673',
        'U [W/M2k]',
        '',
    ),
    (
        'Μετάδοση φωτός - αντανάκλαση φωτός / Light transmission- Light reflection',
        'EN 410',
        'τv-ρv (%)',
        '',
    ),
    (
        'Ηλιακός Συντελεστής / Αντανάκλαση ενέργειας / Energy solar factor / Energy reflection',
        'EN 410',
        'g- pe (%)',
        '',
    ),
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


class En1279Settings(models.Model):
    """Ρυθμίσεις εντύπου EN 1279-5 (singleton)."""

    logo = models.ImageField(
        upload_to='documents/en1279/logo/',
        blank=True,
        null=True,
        verbose_name='Λογότυπο',
    )
    logo_as_watermark = models.BooleanField(
        default=False,
        verbose_name='Υδατογράφημα',
    )
    signature = models.ImageField(
        upload_to='documents/en1279/signature/',
        blank=True,
        null=True,
        verbose_name='Υπογραφή',
    )
    ce_mark = models.ImageField(
        upload_to='documents/en1279/ce/',
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
    standard_intro = models.TextField(
        default=EN1279_DEFAULT_STANDARD_INTRO,
        verbose_name='Κείμενο προτύπου',
    )
    standard_code = models.CharField(
        max_length=50,
        default=EN1279_DEFAULT_STANDARD_CODE,
        verbose_name='Κωδικός προτύπου',
    )
    product_name_label = models.TextField(
        default=EN1279_DEFAULT_PRODUCT_NAME_LABEL,
        verbose_name='Περιγραφή προϊόντος - Τίτλος',
    )
    product_name_value = models.TextField(
        default=EN1279_DEFAULT_PRODUCT_NAME_VALUE,
        verbose_name='Περιγραφή προϊόντος - Κείμενο',
    )
    designation_label = models.TextField(
        default=EN1279_DEFAULT_DESIGNATION_LABEL,
        verbose_name='Τύπος προϊόντος - Τίτλος',
    )
    col_characteristic = models.CharField(
        max_length=120,
        default=EN1279_DEFAULT_COL_CHARACTERISTIC,
        verbose_name='Στήλη ιδιότητας',
    )
    col_spec = models.CharField(
        max_length=120,
        default=EN1279_DEFAULT_COL_SPEC,
        verbose_name='Στήλη προδιαγραφής',
    )
    col_units = models.CharField(
        max_length=80,
        default=EN1279_DEFAULT_COL_UNITS,
        verbose_name='Στήλη μονάδων',
    )
    col_performance = models.CharField(
        max_length=120,
        default=EN1279_DEFAULT_COL_PERFORMANCE,
        verbose_name='Στήλη απόδοσης',
    )
    npd_note = models.CharField(
        max_length=120,
        default=EN1279_DEFAULT_NPD_NOTE,
        verbose_name='Σημείωση NPD',
    )

    # Γραμμές 1–13 πίνακα (κείμενα ρυθμίσεων)
    row_1_characteristic = models.TextField(default=EN1279_ROW_DEFAULTS[0][0])
    row_1_spec = models.CharField(max_length=80, default=EN1279_ROW_DEFAULTS[0][1])
    row_1_units = models.CharField(max_length=40, default=EN1279_ROW_DEFAULTS[0][2])
    row_1_performance = models.CharField(max_length=80, default=EN1279_ROW_DEFAULTS[0][3], blank=True)

    row_2_characteristic = models.TextField(default=EN1279_ROW_DEFAULTS[1][0])
    row_2_spec = models.CharField(max_length=80, default=EN1279_ROW_DEFAULTS[1][1])
    row_2_units = models.CharField(max_length=40, default=EN1279_ROW_DEFAULTS[1][2])
    row_2_performance = models.CharField(max_length=80, default=EN1279_ROW_DEFAULTS[1][3], blank=True)

    row_3_characteristic = models.TextField(default=EN1279_ROW_DEFAULTS[2][0])
    row_3_spec = models.CharField(max_length=80, default=EN1279_ROW_DEFAULTS[2][1])
    row_3_units = models.CharField(max_length=40, default=EN1279_ROW_DEFAULTS[2][2])
    row_3_performance = models.CharField(max_length=80, default=EN1279_ROW_DEFAULTS[2][3], blank=True)

    row_4_characteristic = models.TextField(default=EN1279_ROW_DEFAULTS[3][0])
    row_4_spec = models.CharField(max_length=80, default=EN1279_ROW_DEFAULTS[3][1])
    row_4_units = models.CharField(max_length=40, default=EN1279_ROW_DEFAULTS[3][2])
    row_4_performance = models.CharField(max_length=80, default=EN1279_ROW_DEFAULTS[3][3], blank=True)

    row_5_characteristic = models.TextField(default=EN1279_ROW_DEFAULTS[4][0])
    row_5_spec = models.CharField(max_length=80, default=EN1279_ROW_DEFAULTS[4][1])
    row_5_units = models.CharField(max_length=40, default=EN1279_ROW_DEFAULTS[4][2])
    row_5_performance = models.CharField(max_length=80, default=EN1279_ROW_DEFAULTS[4][3], blank=True)

    row_6_characteristic = models.TextField(default=EN1279_ROW_DEFAULTS[5][0])
    row_6_spec = models.CharField(max_length=80, default=EN1279_ROW_DEFAULTS[5][1])
    row_6_units = models.CharField(max_length=40, default=EN1279_ROW_DEFAULTS[5][2])
    row_6_performance = models.CharField(max_length=80, default=EN1279_ROW_DEFAULTS[5][3], blank=True)

    row_7_characteristic = models.TextField(default=EN1279_ROW_DEFAULTS[6][0])
    row_7_spec = models.CharField(max_length=80, default=EN1279_ROW_DEFAULTS[6][1])
    row_7_units = models.CharField(max_length=40, default=EN1279_ROW_DEFAULTS[6][2])
    row_7_performance = models.CharField(max_length=80, default=EN1279_ROW_DEFAULTS[6][3], blank=True)

    row_8_characteristic = models.TextField(default=EN1279_ROW_DEFAULTS[7][0])
    row_8_spec = models.CharField(max_length=80, default=EN1279_ROW_DEFAULTS[7][1])
    row_8_units = models.CharField(max_length=40, default=EN1279_ROW_DEFAULTS[7][2])
    row_8_performance = models.CharField(max_length=80, default=EN1279_ROW_DEFAULTS[7][3], blank=True)

    row_9_characteristic = models.TextField(default=EN1279_ROW_DEFAULTS[8][0])
    row_9_spec = models.CharField(max_length=80, default=EN1279_ROW_DEFAULTS[8][1])
    row_9_units = models.CharField(max_length=40, default=EN1279_ROW_DEFAULTS[8][2])
    row_9_performance = models.CharField(max_length=80, default=EN1279_ROW_DEFAULTS[8][3], blank=True)

    row_10_characteristic = models.TextField(default=EN1279_ROW_DEFAULTS[9][0])
    row_10_spec = models.CharField(max_length=80, default=EN1279_ROW_DEFAULTS[9][1])
    row_10_units = models.CharField(max_length=40, default=EN1279_ROW_DEFAULTS[9][2])
    row_10_performance = models.CharField(max_length=80, default=EN1279_ROW_DEFAULTS[9][3], blank=True)

    row_11_characteristic = models.TextField(default=EN1279_ROW_DEFAULTS[10][0])
    row_11_spec = models.CharField(max_length=80, default=EN1279_ROW_DEFAULTS[10][1])
    row_11_units = models.CharField(max_length=40, default=EN1279_ROW_DEFAULTS[10][2])

    row_12_characteristic = models.TextField(default=EN1279_ROW_DEFAULTS[11][0])
    row_12_spec = models.CharField(max_length=80, default=EN1279_ROW_DEFAULTS[11][1])
    row_12_units = models.CharField(max_length=40, default=EN1279_ROW_DEFAULTS[11][2])

    row_13_characteristic = models.TextField(default=EN1279_ROW_DEFAULTS[12][0])
    row_13_spec = models.CharField(max_length=80, default=EN1279_ROW_DEFAULTS[12][1])
    row_13_units = models.CharField(max_length=40, default=EN1279_ROW_DEFAULTS[12][2])

    updated_at = models.DateTimeField(auto_now=True, verbose_name='Τελευταία ενημέρωση')

    class Meta:
        verbose_name = 'Ρυθμίσεις EN 1279-5'
        verbose_name_plural = 'Ρυθμίσεις EN 1279-5'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def get_table_rows(self, document=None):
        """Επιστρέφει τις 13 γραμμές πίνακα για εκτύπωση."""
        rows = []
        for index in range(1, 14):
            row = {
                'num': index,
                'characteristic': getattr(self, f'row_{index}_characteristic'),
                'spec': getattr(self, f'row_{index}_spec'),
                'units': getattr(self, f'row_{index}_units'),
                'performance': '',
                'is_input': index >= 11,
            }
            if index <= 10:
                row['performance'] = getattr(self, f'row_{index}_performance')
            elif document is not None:
                if index == 11:
                    row['performance'] = document.thermal_performance
                elif index == 12:
                    row['performance'] = document.light_performance
                else:
                    row['performance'] = document.energy_performance
            rows.append(row)
        return rows

    def __str__(self):
        return 'Ρυθμίσεις EN 1279-5'


class En1279Document(models.Model):
    """Έντυπο απόδοσης σύμφωνα με το πρότυπο EN 1279-5."""

    document_number = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='Αριθμός Εντύπου',
    )
    product_designation = models.CharField(
        max_length=255,
        verbose_name='Τύπος προϊόντος',
    )
    thermal_performance = models.CharField(
        max_length=100,
        verbose_name='Συντελεστής θερμοαγωγιμότητας (U)',
    )
    light_performance = models.CharField(
        max_length=100,
        verbose_name='Μετάδοση φωτός - αντανάκλαση φωτός',
    )
    energy_performance = models.CharField(
        max_length=100,
        verbose_name='Ηλιακός συντελεστής / Αντανάκλαση ενέργειας',
    )
    show_signature = models.BooleanField(
        default=True,
        verbose_name='Εμφάνιση Υπογραφής',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ημερομηνία Δημιουργίας')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='en1279_created',
        verbose_name='Δημιουργήθηκε από',
    )

    class Meta:
        verbose_name = 'Έντυπο EN 1279-5'
        verbose_name_plural = 'Έντυπα EN 1279-5'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.document_number} - {self.product_designation}'

    def save(self, *args, **kwargs):
        if not self.document_number:
            today = timezone.localdate()
            year_suffix = today.strftime('%y')
            suffix = f'-{year_suffix}'
            prefix = 'EN'

            max_number = 0
            for document_number in En1279Document.objects.filter(
                document_number__endswith=suffix,
            ).values_list('document_number', flat=True):
                try:
                    # EN0001-26
                    core = document_number.replace(prefix, '', 1).split('-', 1)[0]
                    sequence = int(core)
                except (ValueError, IndexError):
                    continue
                max_number = max(max_number, sequence)

            self.document_number = f'{prefix}{max_number + 1:04d}{suffix}'
        super().save(*args, **kwargs)

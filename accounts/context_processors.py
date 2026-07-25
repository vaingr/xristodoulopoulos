def client_name(request):
    """Context processor για το όνομα πελάτη"""
    try:
        with open('client_name.txt', 'r', encoding='utf-8') as f:
            client_name = f.read().strip() or 'DataLab'
    except FileNotFoundError:
        client_name = 'DataLab'

    return {'client_name': client_name}


def app_name(request):
    """Context processor για το όνομα εφαρμογής"""
    try:
        with open('app_name.txt', 'r', encoding='utf-8') as f:
            app_name = f.read().strip() or 'DataLab'
    except FileNotFoundError:
        app_name = 'DataLab'

    return {'app_name': app_name}


def partner_name(request):
    """Context processor για το όνομα συνεργάτη"""
    try:
        with open('partner_name.txt', 'r', encoding='utf-8') as f:
            partner_name = f.read().strip() or 'DataLab'
    except FileNotFoundError:
        partner_name = 'DataLab'

    return {'partner_name': partner_name}


def sms_enabled(request):
    """Context processor για έλεγχο αν το SMS είναι ενεργοποιημένο."""
    from .module_settings import get_module_flags
    return {'sms_enabled': get_module_flags().get('sms', True)}


def customers_enabled(request):
    """Context processor για modules sidebar και συμβατότητα πελατών/SMS."""
    from .module_settings import get_module_flags
    flags = get_module_flags()
    return {
        'customers_enabled': flags.get('customers', True),
        'sms_enabled': flags.get('sms', True),
        'sidebar_modules': flags,
    }

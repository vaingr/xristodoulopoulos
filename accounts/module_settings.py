"""Ρυθμίσεις ορατότητας modules για απλούς χρήστες (αποθήκευση στο .env)."""

SIDEBAR_MODULES = [
    {
        'key': 'customers',
        'env_key': 'CUSTOMERS_ENABLED',
        'label': 'Πελάτες',
        'icon': 'fas fa-users',
        'description': 'Εμφάνιση της επιλογής «Πελάτες» στο sidebar.',
    },
    {
        'key': 'products',
        'env_key': 'MODULE_PRODUCTS',
        'label': 'Προϊόντα',
        'icon': 'fas fa-box',
        'description': 'Εμφάνιση της επιλογής «Προϊόντα» στο sidebar.',
    },
    {
        'key': 'warehouse_materials',
        'env_key': 'MODULE_WAREHOUSE_MATERIALS',
        'label': 'Αποθήκη Υλικών',
        'icon': 'fas fa-warehouse',
        'description': 'Εμφάνιση της επιλογής «Αποθήκη Υλικών» στο sidebar.',
    },
    {
        'key': 'warehouse_finished',
        'env_key': 'MODULE_WAREHOUSE_FINISHED',
        'label': 'Αποθήκη Έτοιμων Προϊόντων',
        'icon': 'fas fa-boxes-stacked',
        'description': 'Εμφάνιση της επιλογής «Αποθήκη Έτοιμων Προϊόντων» στο sidebar.',
    },
    {
        'key': 'offers',
        'env_key': 'MODULE_OFFERS',
        'label': 'Προσφορές',
        'icon': 'fas fa-file-invoice',
        'description': 'Εμφάνιση της επιλογής «Προσφορές» στο sidebar.',
    },
    {
        'key': 'documents',
        'env_key': 'MODULE_DOCUMENTS',
        'label': 'Έντυπα',
        'icon': 'fas fa-file-alt',
        'description': 'Εμφάνιση της επιλογής «Έντυπα» στο sidebar.',
    },
    {
        'key': 'task_scheduling',
        'env_key': 'MODULE_TASK_SCHEDULING',
        'label': 'Προγραμματισμός Εργασιών',
        'icon': 'fas fa-calendar-check',
        'description': 'Εμφάνιση της επιλογής «Προγραμματισμός Εργασιών» στο sidebar.',
    },
    {
        'key': 'sms',
        'env_key': 'SMS_ENABLED',
        'label': 'SMS',
        'icon': 'fas fa-sms',
        'description': 'Εμφάνιση της επιλογής «SMS» στο sidebar.',
    },
]

ENV_SECTION_HEADER = '# Sidebar Modules Settings'


def _parse_bool(value, default=True):
    if value is None:
        return default
    return str(value).strip().strip('"').strip("'").lower() in ('true', '1', 'yes', 'on')


def read_env_values():
    values = {}
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                key, value = line.split('=', 1)
                values[key.strip()] = value.strip().strip('"').strip("'")
    except FileNotFoundError:
        pass
    return values


def get_module_flags():
    env = read_env_values()
    return {
        module['key']: _parse_bool(env.get(module['env_key']), True)
        for module in SIDEBAR_MODULES
    }


def get_modules_for_form():
    flags = get_module_flags()
    return [
        {
            **module,
            'enabled': flags[module['key']],
        }
        for module in SIDEBAR_MODULES
    ]


def save_module_flags(flags):
    """Αποθηκεύει τα flags modules στο .env, διατηρώντας τις υπόλοιπες ρυθμίσεις."""
    env_keys = {module['env_key'] for module in SIDEBAR_MODULES}
    section_headers = {ENV_SECTION_HEADER, '# Customers Module Settings'}

    existing_lines = []
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            existing_lines = f.read().splitlines()
    except FileNotFoundError:
        pass

    filtered = []
    skip_section = False
    for line in existing_lines:
        stripped = line.strip()

        if stripped in section_headers:
            skip_section = True
            continue

        if skip_section:
            if stripped.startswith('#') and stripped not in section_headers:
                skip_section = False
            else:
                continue

        if any(
            stripped.startswith(f'{key}=') or stripped.startswith(f'{key} =')
            for key in env_keys
        ):
            continue

        filtered.append(line)

    while filtered and not filtered[-1].strip():
        filtered.pop()

    with open('.env', 'w', encoding='utf-8') as f:
        for line in filtered:
            f.write(line + '\n')
        if filtered:
            f.write('\n')
        f.write(f'{ENV_SECTION_HEADER}\n')
        for module in SIDEBAR_MODULES:
            enabled = bool(flags.get(module['key'], True))
            f.write(f"{module['env_key']}={'true' if enabled else 'false'}\n")

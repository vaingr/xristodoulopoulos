def generate_dop_pdf(dop, request):
    from django.urls import reverse

    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError(
            'Το Playwright δεν είναι εγκατεστημένο. '
            'Εκτελέστε: pip install playwright && playwright install chromium'
        ) from exc

    print_url = request.build_absolute_uri(
        reverse('documents:dop_print', args=[dop.pk]) + '?pdf=1'
    )
    base_url = request.build_absolute_uri('/')

    auth_cookies = []
    for name in ('sessionid', 'csrftoken'):
        value = request.COOKIES.get(name)
        if value:
            auth_cookies.append({
                'name': name,
                'value': value,
                'url': base_url,
            })

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            context = browser.new_context()
            if auth_cookies:
                context.add_cookies(auth_cookies)
            page = context.new_page()
            page.goto(print_url, wait_until='networkidle', timeout=60000)
            page.wait_for_selector('.a4-page', timeout=60000)
            page.wait_for_timeout(300)
            pdf_bytes = page.pdf(
                format='A4',
                print_background=True,
                margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'},
                prefer_css_page_size=True,
            )
            browser.close()
    except Exception as exc:
        if 'Executable doesn' in str(exc) or 'BrowserType.launch' in str(exc):
            raise RuntimeError(
                'Δεν βρέθηκε το Chromium στον server. '
                'Εκτελέστε ως ο χρήστης της εφαρμογής: python -m playwright install chromium'
            ) from exc
        raise

    return pdf_bytes

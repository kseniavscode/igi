from pages.models import CompanyInfo


def company_info(request):
    try:
        info = CompanyInfo.objects.first()
    except Exception:
        info = None
    return {'company_info': info}
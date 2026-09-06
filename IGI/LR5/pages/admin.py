from django.contrib import admin
from .models import CompanyInfo, Certificate, Article, FAQ, Vacancy, Review, PromoCode, CompanyPartner


class CertificateInline(admin.TabularInline):
    model = Certificate
    extra = 1

@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name', 'description']
    inlines = [CertificateInline]


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['title', 'company']
    list_filter = ['company']
    search_fields = ['title']

# Register your models here.
admin.site.register(Article)
admin.site.register(FAQ)
admin.site.register(Vacancy)
admin.site.register(Review)
admin.site.register(PromoCode)
admin.site.register(CompanyPartner)
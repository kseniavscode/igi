from django.contrib import admin
from .models import CompanyInfo, Article, FAQ, Vacancy, Review, PromoCode

# Register your models here.
admin.site.register(CompanyInfo)
admin.site.register(Article)
admin.site.register(FAQ)
admin.site.register(Vacancy)
admin.site.register(Review)
admin.site.register(PromoCode)

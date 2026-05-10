from django.shortcuts import render
from .models import Article, CompanyInfo, FAQ, Employee, Vacancy, Review, PromoCode

# Create your views here.

def home_page(request):
    """Main page with the last article"""
    last_article = Article.objects.order_by('-publishing_date').first()
    return render(request, 'pages/home.html', {'article': last_article})
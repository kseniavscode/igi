from django.shortcuts import render
from .models import Article, CompanyInfo, FAQ, Vacancy, Review, PromoCode

# Create your views here.

def news_page(request):
    """Main page with the last article"""
    articles = Article.objects.all()
    return render(request, 'pages/news.html', {'articles': articles})




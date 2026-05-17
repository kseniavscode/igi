from django.shortcuts import render, redirect
from .models import Article, CompanyInfo, FAQ, Vacancy, Review, PromoCode
from store.models import Employee
from django.db.models import Q

from .forms import ReviewForm, QuestionForm, AnswerForm

import logging

# Create your views here.
logger = logging.getLogger('pages')

def news_page(request):
    """News with artcles"""
    articles = Article.objects.all().order_by('-publishing_date')
    logger.debug(f"NEWS page accessed by {request.user.username if request.user.is_authenticated else 'Anonymous'}")
    return render(request, 'pages/news.html', {'articles': articles})

def about_company(request):
    company_info = CompanyInfo.objects.first()
    logger.debug(f"ABOUT COMPANY page accessed by {request.user.username if request.user.is_authenticated else 'Anonymous'}")
    return render(request, 'pages/about.html', {'info': company_info})

def faq_page(request):
    """FAQ """

    if request.method == 'POST':
        if 'ask_question' in request.POST and request.user.is_authenticated:
            form = QuestionForm(request.POST)
            if form.is_valid():
                new_q = form.save(commit=False)
                new_q.user = request.user
                new_q.save()

                logger.info(f"New question asked by {request.user.username}")

                return redirect('faq')
            
        if 'answer_question' in request.POST and request.user.is_staff:
            question_id = request.POST.get('question_id')
            instance = FAQ.objects.get(id=question_id)
            form = AnswerForm(request.POST, instance=instance)
            if form.is_valid():
                form.save()

                logger.info(f"Staff {request.user.username} answered question ID {question_id}")

                return redirect('faq')
            



    faqs_answered = FAQ.objects.filter(answer__isnull=False).exclude(answer='').order_by('-date')
    faqs_unanswered = FAQ.objects.filter(Q(answer__isnull=True) | Q(answer=''))

    logger.debug(f"FAQ page accessed by {request.user.username if request.user.is_authenticated else 'Anonymous'}")

    context = {
        'faqs': faqs_answered,
        'unanswered': faqs_unanswered,
        'question_form': QuestionForm(),
        'answer_form': AnswerForm(),
    }

    return render(request, 'pages/faq.html', context)

def contacts_page(request):
    """Contacts from store.Employee"""
    employees = Employee.objects.all()
    logger.debug(f"CONTACTS page accessed by {request.user.username if request.user.is_authenticated else 'Anonymous'}")
    return render(request, 'pages/contacts.html', {'employees': employees})

def vacancies_page(request):
    """Vacancies"""
    vacancies = Vacancy.objects.all()
    logger.debug(f"VACANCIES page accessed by {request.user.username if request.user.is_authenticated else 'Anonymous'}")
    return render(request, 'pages/vacancies.html', {'vacancies': vacancies})

def reviews_page(request):
    """Revies"""

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.name = request.user.username 
                review.save()

                logger.info(f"Review added by {request.user.username}. Rating: {review.rating}")

                return redirect('reviews')

            else:
                logger.error(f"Form validation error in reviews: {form.errors}")
                
        else:
            logger.warning("Anonymous user attempted to post a review!")
            return redirect('login')
        

    reviews = Review.objects.all().order_by('-date')
    form = ReviewForm()
    logger.debug(f"REVIEWS page accessed by {request.user.username if request.user.is_authenticated else 'Anonymous'}")
    return render(request, 'pages/reviews.html', {'reviews': reviews, 'form': form})

def promo_page(request):
    """PROMOCODES"""
    active_promos = PromoCode.objects.filter(is_active=True)
    archived_promos = PromoCode.objects.filter(is_active=False)
    logger.debug(f"PROMOCODES page accessed by {request.user.username if request.user.is_authenticated else 'Anonymous'}")
    return render(request, 'pages/promo.html', {
        'active_promos': active_promos,
        'archived_promos': archived_promos
    })

def privacy_policy(request):
    """Policy"""
    logger.debug(f"POLICY page accessed by {request.user.username if request.user.is_authenticated else 'Anonymous'}")
    return render(request, 'pages/privacy_policy.html')


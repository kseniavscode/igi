from django.urls import path
from . import views

urlpatterns = [
    path('news/', views.news_page, name='news'),
    path('about_company/', views.about_company, name='about'),
    path('faq/', views.faq_page, name='faq'),
    path('contacts/', views.contacts_page, name='contacts'),
    path('vacancies/', views.vacancies_page, name='vacancies'),
    path('reviews/', views.reviews_page, name='reviews'),
    path('promo/', views.promo_page, name='promo'),
    path('privacy/', views.privacy_policy, name='privacy')
]

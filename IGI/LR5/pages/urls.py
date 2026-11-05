from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r"^news/$$", views.news_page, name="news"),
    re_path(r"^about_company/$", views.about_company, name="about"),
    re_path(r"^faq/$", views.faq_page, name="faq"),
    re_path(r"^contacts/$", views.contacts_page, name="contacts"),
    re_path(r"^vacancies/$", views.vacancies_page, name="vacancies"),
    re_path(r"^reviews/$", views.reviews_page, name="reviews"),
    re_path(r"^promo/$", views.promo_page, name="promo"),
    re_path(r"^privacy/$", views.privacy_policy, name="privacy"),
    re_path(r"^form-builder/$", views.form_builder_page, name='form_builder'),
    re_path(r"^cubes/$", views.cubes_task_page, name='cubes'),
    re_path(r"^chart/$", views.chart_page, name='chart'),
]

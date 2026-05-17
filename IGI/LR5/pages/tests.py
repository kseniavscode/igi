import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Article, FAQ, Review, PromoCode, Vacancy, CompanyInfo
from .forms import QuestionForm, ReviewForm
from store.models import Employee

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='password')

@pytest.fixture
def staff_user(db):
    return User.objects.create_user(username='staff', password='password', is_staff=True)



@pytest.mark.django_db
@pytest.mark.parametrize("url_name", [
    'news', 'about', 'contacts', 'vacancies', 'promo', 'privacy'
])
def test_simple_pages_get(client, url_name):
    url = reverse(url_name)
    response = client.get(url)
    assert response.status_code == 200



@pytest.mark.django_db
class TestFAQ:
    def test_faq_display_separation(self, client):
        """Проверка, что отвеченные и неотвеченные вопросы разделяются"""
        FAQ.objects.create(question="Q1", answer="A1") # Отвеченный
        FAQ.objects.create(question="Q2", answer="")   # Неотвеченный
        
        response = client.get(reverse('faq'))
        assert len(response.context['faqs']) == 1
        assert len(response.context['unanswered']) == 1

    def test_ask_question_authenticated(self, client, user):
        
        client.login(username='testuser', password='password')
        url = reverse('faq')
        data = {
            'ask_question': True, 
            'question': 'How are you?' 
        }
        response = client.post(url, data)
        assert response.status_code == 302
        assert FAQ.objects.filter(question='How are you?', user=user).exists()

    def test_answer_question_staff_only(self, client, staff_user, user):

        q = FAQ.objects.create(question="Help me", user=user)
        client.login(username='staff', password='password')
        
        url = reverse('faq')
        data = {
            'answer_question': True,
            'question_id': q.id,
            'answer': 'Fixed!'
        }
        response = client.post(url, data)
        q.refresh_from_db()
        assert q.answer == 'Fixed!'


@pytest.mark.django_db
class TestReviews:
    def test_post_review_authenticated(self, client, user):
        client.login(username='testuser', password='password')
        url = reverse('reviews')
        data = {
            'text': 'Great store!',
            'rating': 5
        }
        response = client.post(url, data)
        assert response.status_code == 302
        
        review = Review.objects.get(text='Great store!')
        assert review.user == user
        assert review.name == 'testuser'

    def test_post_review_anonymous_redirects(self, client):
        
        url = reverse('reviews')
        data = {'text': 'Anon review', 'rating': 1}
        response = client.post(url, data)
        assert response.status_code == 302
        assert 'login' in response.url


@pytest.mark.django_db
def test_promo_page_filtering_for_anonymous(client):

    PromoCode.objects.create(code="ACTIVE10", is_active=True, discode=10)
    PromoCode.objects.create(code="OLD50", is_active=False, discode=50)
    
    response = client.get(reverse('promo'))
    
    assert response.status_code == 200
    
    assert response.context['active_promos'].count() == 1
    assert response.context['archived_promos'].count() == 1
    
    content = response.content.decode()
    assert "ACTIVE10" in content    
    assert "OLD50" not in content   

@pytest.mark.django_db
def test_promo_page_filtering_for_staff(client, staff_user):
    PromoCode.objects.create(code="ACTIVE10", is_active=True, discode=10)
    PromoCode.objects.create(code="OLD50", is_active=False, discode=50)
    
    client.login(username='staff', password='password') 
    response = client.get(reverse('promo'))
    
    content = response.content.decode()
    assert "ACTIVE10" in content 
    assert "OLD50" in content    
    assert "Archived PromoCodes" in content



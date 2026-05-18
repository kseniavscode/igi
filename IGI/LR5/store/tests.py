from django.test import TestCase
import pytest
from django.urls import reverse

from django.contrib.auth.models import User
from .models import Book, Client, BookInstance, Genre, Order, Waitlist, PickupPoint
import re

from django.contrib.messages import get_messages

# Create your tests here.

@pytest.fixture
def regular_user(db):
    """Create user"""
    return User.objects.create_user(username='testuser', password='password')

@pytest.fixture
def staff_user(db):
    """Create staff"""
    return User.objects.create_user(username='staff', password='password', is_staff=True)

@pytest.fixture
def user_client(db, regular_user):
    """Создаем профиль клиента для testuser"""
    return Client.objects.create(
        user=regular_user, 
        phone="123456789", 
        city="Minsk", 
        birth_date="1990-01-01"
    )

@pytest.fixture
def book_with_instance(db):
    """Create a book and an instance"""
    book = Book.objects.create(title="Test Book", isbn="1112223334445", price=100.0)
    instance = BookInstance.objects.create(book=book, status='a')
    return book, instance


# Check decorator
@pytest.mark.django_db
def test_import_books_forbidden_for_regular_user(client, regular_user):

    client.login(username='testuser', password='password')

    url = reverse('import_books')
    response = client.get(url)

    assert response.status_code == 302
    assert response.url == reverse('book_list')


@pytest.mark.django_db
def test_book_list(client):
    url = reverse('book_list')
    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_book_details(client):

    book = Book.objects.create(title='Title', isbn="1234567890123", price=25.0)

    url = reverse('book_details', kwargs={'pk': book.pk})
    response = client.get(url)

    assert response.status_code == 200
    assert "Title" in response.content.decode()




@pytest.mark.parametrize("price_input, expected_result", [
    ("10.50", True),  
    ("100", True),    
    ("abc", False),   
    ("10,50", False), 
    ("-10", False),   
])
def test_price_validation(price_input, expected_result):

    assert bool(re.match(r'^\d+(\.\d{1,2})?$', price_input)) == expected_result




@pytest.mark.django_db
def test_updated_book_successfully(client, staff_user):

    client.login(username='staff', password='password')

    book = Book.objects.create(title='Title', isbn="password567890123", price=25.0)

    url = reverse('update_book', kwargs={'pk': book.pk})

    data = {
        'title': 'New Cool Title',
        'imprint': 'Modern Publisher',
        'isbn': '9999999999999',
        'price': '45.50',
        'language': 'RUSSIAN',
        'genres': 'Drama, Rom',
        'authors': 'Pushkin, Tolstoy',
        'summary': 'New description'
    }

    response = client.post(url, data)

    assert response.status_code == 302

    book.refresh_from_db()

    assert book.title == 'New Cool Title'
    assert book.price == 45.50
    assert book.language.name == 'RUSSIAN'
    assert book.authors.count() == 2
    assert book.genre.count() == 2

@pytest.mark.django_db
@pytest.mark.parametrize("invalid_data, error_message", [
    ({'authors': 'Pushkin123'}, 'Enter rigth information about authors'),
    ({'genres': 'Drama!!!'}, 'Enter rigth information about genres'),     
    ({'language': 'RU 1'}, 'Enter rigth information about language'),   
    ({'price': '10,50'}, 'Enter rigth information about price'),        
    ({'isbn': '123'}, 'Enter rigth information about isbn'),             
    ({'imprint': 'Pub@lisher'}, 'Enter rigth information about publishing house'), 
    ({'title': 'Title <script>'}, 'Enter rigth information about a book`s title'), 
    ({'title': 'A Queen`s party'}, 'Success: Data is updated'), 
])
def test_update_book_validation(client, staff_user, invalid_data, error_message) :
    client.login(username='staff', password='password')
    book = Book.objects.create(title="Valid Title", isbn="1111111111111", price=10.0)
    url = reverse('update_book', kwargs={'pk': book.pk})

    valid_payload = {
        'title': 'Valid Title',
        'imprint': 'Publisher',
        'isbn': '1111111111111',
        'price': '10.00',
        'language': 'English',
        'genres': 'Genre',
        'authors': 'Author',
        'summary': 'Summary'
    }

    valid_payload.update(invalid_data)

    response = client.post(url, valid_payload)

    assert response.status_code == 302

    messages = list(get_messages(response.wsgi_request))
    assert any(error_message in m.message for m in messages)

    book.refresh_from_db()
    if 'price' in invalid_data:
        assert book.price == 10.00




@pytest.mark.django_db
def test_delete_book_as_staff(client, staff_user, book_with_instance):
    book, instance = book_with_instance
    client.login(username='staff', password='password')
    
    url = reverse('delete_book', kwargs={'pk': book.pk})
    response = client.get(url)
    
    assert response.status_code == 302
    assert not Book.objects.filter(pk=book.pk).exists()
    assert not BookInstance.objects.filter(pk=instance.pk).exists()

@pytest.mark.django_db
def test_delete_book_forbidden_for_regular_user(client, regular_user):
    book = Book.objects.create(title="Title", isbn="1234567890123", price=10.0)
    client.login(username='testuser', password='password')
    
    url = reverse('delete_book', kwargs={'pk': book.pk})
    response = client.get(url)
    
    assert response.status_code == 302
    assert Book.objects.filter(pk=book.pk).exists()

@pytest.mark.django_db
class TestOrderProcess:
    
    def test_add_to_orders_available(self, client, regular_user, user_client, book_with_instance):
        
        book, instance = book_with_instance
        client.login(username='testuser', password='password')
        
        url = reverse('add_to_orders', kwargs={'pk': book.pk})
        response = client.get(url)
        
        instance.refresh_from_db()
        
        assert instance.status == 'r'
        assert Order.objects.filter(client=user_client, status='n').exists()
        assert response.url == reverse('my_orders')

    def test_add_to_orders_waitlist(self, client, regular_user, user_client):
        
        book = Book.objects.create(title="No stock", isbn="000", price=50.0)
        
        client.login(username='testuser', password='password')
        
        url = reverse('add_to_orders', kwargs={'pk': book.pk})
        response = client.get(url)
        
        assert Waitlist.objects.filter(client=user_client, book=book).exists()
        assert response.url == reverse('book_details', kwargs={'pk': book.pk})

    def test_confirm_order(self, client, regular_user, user_client):

        order = Order.objects.create(client=user_client, status='n')
        point = PickupPoint.objects.create(
            address="Central St. 1", 
            city="Minsk", 
            opening_hours="9-21", 
            map_coordinates="0,0"
        ) 

        client.login(username='testuser', password='password')
        url = reverse('confirm_order', kwargs={'pk': order.pk})
        data = {
            'delivery_method': 's',     
            'pickup_point': point.id,   
            'promo_code': ''           
        }

        response = client.post(url, data)
        
        assert response.status_code == 302
        assert response.url == reverse('my_orders')
        
        order.refresh_from_db()
        assert order.status == 'p'
        assert order.delivery_method == 's'
        assert order.pickup_point == point
        assert order.final_price is not None

    def test_cancel_order(self, client, regular_user, user_client, book_with_instance):
        book, instance = book_with_instance
        order = Order.objects.create(client=user_client, status='n')
        instance.status = 'r'
        instance.order = order
        instance.save()
        
        client.login(username='testuser', password='password')
        client.get(reverse('cancel_order', kwargs={'pk': order.pk}))
        
        order.refresh_from_db()
        instance.refresh_from_db()
        assert order.status == 'c'
        assert instance.status == 'a' 
        assert instance.order is None



@pytest.mark.django_db
def test_complete_order_by_staff(client, staff_user, user_client, book_with_instance):
    book, instance = book_with_instance
    order = Order.objects.create(client=user_client, status='p')
    instance.status = 'r'
    instance.order = order
    instance.save()
    
    client.login(username='staff', password='password')
    client.get(reverse('complete_order', kwargs={'pk': order.pk}))
    
    order.refresh_from_db()
    instance.refresh_from_db()
    assert order.status == 'd' 
    assert instance.status == 's' 

@pytest.mark.django_db
def test_order_management_search(client, staff_user, user_client):
    Order.objects.create(client=user_client, status='p') 
    client.login(username='staff', password='password')
    
    url = reverse('order_management') + "?search=123"
    response = client.get(url)
    assert len(response.context['orders']) == 1
    
    url = reverse('order_management') + "?search=UnknownUser"
    response = client.get(url)
    assert len(response.context['orders']) == 0

@pytest.mark.django_db
def test_statistic_view_renders(client, staff_user):
    
    client.login(username='staff', password='password')
    url = reverse('stats')
    response = client.get(url)
    
    assert response.status_code == 200
    assert 'total_revenue' in response.context
    assert 'forecast_value' in response.context









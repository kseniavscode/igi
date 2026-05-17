from django.db import models
import uuid
from django.contrib.auth.models import User
from django.utils import timezone

from pages.models import PromoCode
# Create your models here.


class Author(models.Model):
    """Model of Author class"""
    name = models.CharField(max_length=100, verbose_name="Name of author")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Date of birth")
    date_of_death = models.DateField(null=True, blank=True, verbose_name="Date of death")

    def __str__(self):
        return self.name
    
class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name="Type of genre")

    def __str__(self):
        return self.name
    

class Language(models.Model):
    name = models.CharField(max_length=100, verbose_name="Language")

    def __str__(self):
        return self.name 


class Book(models.Model):
    """Class of book"""

    title = models.CharField(max_length=150, verbose_name="Title of book")
    cover = models.ImageField(upload_to='books/', null=True, blank=True, verbose_name="Book cover")
    summary = models.TextField(verbose_name="Annotation")
    imprint = models.CharField(max_length=100, blank=True, verbose_name="Publishing House")
    isbn = models.CharField(max_length=13, verbose_name="ISBN")

    genre = models.ManyToManyField(Genre, verbose_name="Genres")
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, verbose_name="Language")
    authors = models.ManyToManyField(Author, verbose_name="Authors")

    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Price of book")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class BookInstance(models.Model):
    """A model of specific copy of the book"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique id of this book")
    imprint = models.CharField(max_length=200, verbose_name="Stamp of the publishing house")
    due_back = models.DateField(null=True, blank=True, verbose_name="Possible return date")

    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, verbose_name="Book")

    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True, blank=True, related_name='instances')

    LOAN_STATUS = [
        ("m", "maintenance"),
        ("s", "sold"),
        ("a", "available"),
        ("r", "reserved")
    ]

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default="m", verbose_name="Status")

    def __str__(self):
        return f"{self.id} ({self.book.title})"



class Client(models.Model):
    """Model of profil of client"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Profil")

    phone = models.CharField(max_length=17, verbose_name="Phone number")

    birth_date = models.DateField() 

    address = models.TextField(blank=True, verbose_name="Delivery address (Street, House, Flat)")

    CITY_CHOICES = [
        ('Minsk', 'Minsk'),
        ('Brest', 'Brest'),
        ('Grodno', 'Grodno'),
        ('Gomel', 'Gomel'),
        ('Vitebsk', 'Vitebsk'),
        ('Mogilev', 'Mogilev'),
        ('Baranovichi', 'Baranovichi'),
        ('Borisov', 'Borisov'),
        ('Pinsk', 'Pinsk'),
        ('Orsha', 'Orsha'),
        ('Mozyr', 'Mozyr'),
        ('Soligorsk', 'Soligorsk'),
        ('Lida', 'Lida'),
        ('Molodechno', 'Molodechno'),
    ]

    city = models.CharField(
        max_length=50, 
        choices=CITY_CHOICES, 
        default='Minsk', 
        verbose_name="City"
    )

    def __str__(self):
        return f"{self.user.username} ({self.phone})"
    
    def get_age(self):
        import datetime
        return (datetime.date.today() - self.birth_date).days // 365
    
class Employee(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="User Account", null=True, blank=True)

    full_name = models.CharField(max_length=150, verbose_name="Full- Last- Second name")
    position = models.CharField(max_length=100, verbose_name="Position in this company")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=17, verbose_name="Phone", blank=True)
    description = models.TextField(verbose_name="Work description", blank=True)
    photo = models.ImageField(upload_to='employees/', null=True, blank=True)

    def __str__(self):
        return self.full_name

class PickupPoint(models.Model):
    """Pickiiii upiiiii"""
    address = models.CharField(max_length=255, verbose_name="Address")
    city = models.CharField(max_length=100, verbose_name="City")
    opening_hours = models.CharField(max_length=100, verbose_name="Time of work")
    map_coordinates = models.CharField(max_length=50, help_text="Coordinates in map")

    def __str__(self):
        return f"{self.city}, {self.address}"
    
class Order(models.Model):
    """Model of order"""

    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Client")
    books = models.ManyToManyField(Book, verbose_name="Books in order")

    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date of order")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Processed at")

    delivery_address = models.TextField(blank=True, null=True, verbose_name="Адрес доставки")
    pickup_point = models.ForeignKey(PickupPoint, on_delete=models.SET_NULL, null=True, blank=True)
    promo_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    STATUS_CHOICE = [
        ('n', 'New'),
        ('p', 'In process'),
        ('d', 'Done'),
        ('c', 'Cancel')
    ]

    status = models.CharField(max_length=1, choices=STATUS_CHOICE, default='n', verbose_name='Status of order')


    DELIVERY_CHOICES = [
        ('s', 'Pickup (Self-delivery)'),
        ('c', 'Courier'),
    ]
    delivery_method = models.CharField(max_length=1, choices=DELIVERY_CHOICES, default='s', verbose_name='Delivery method')
        
    def total_price(self):
        total = self.instances.aggregate(total=models.Sum('book__price'))['total'] or 0
        if self.promo_code:
            discount = (total * self.promo_code.discode) / 100
            total -= discount
        return total
    
    def get_group_items(self):
        items =[]
        for book in self.books.all():
            count = self.instances.filter(book=book).count()
            if count > 0:
                items.append({
                    'book': book,
                    'count': count,
                    'total_item_price': book.price * count
                })
        return items

    def __str__(self):
        return f"Order #{self.id} from {self.client.user.username}"

class Waitlist(models.Model):

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_at = models.DateTimeField(default=timezone.now, verbose_name="Date of added at waitlist")

    class Meta:
        unique_together = ('client', 'book')
    def __str__(self):
        return f"{self.client.user.username} waiting for {self.book.title}"
    

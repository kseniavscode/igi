from django.db import models
import uuid
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator

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
    summery = models.CharField(max_length=1500, verbose_name="Annotation")
    imprint = models.CharField(max_length=100, blank=True, verbose_name="Publishing House")
    isbn = models.CharField(max_length=13, verbose_name="ISBN")

    genre = models.ManyToManyField(Genre, verbose_name="Genres")
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, verbose_name="Language")
    authors = models.ManyToManyField(Author, verbose_name="Authors")

    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Price of book")

    def __str__(self):
        return self.title
    

class BookInstance(models.Model):
    """A model of specific copy of the book"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique id of this book")
    imprint = models.CharField(max_length=200, verbose_name="Stamp of the publishing house")
    due_back = models.DateField(null=True, blank=True, verbose_name="Possible return date")

    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True, verbose_name="Book")

    LOAN_STATUS = {
        ("m", "maintenance"),
        ("s", "sold"),
        ("a", "available"),
        ("r", "reserved")
    }

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default="m", verbose_name="Status")

    def __str__(self):
        return f"{self.id} ({self.book.title})"



class Client(models.Model):
    """Model of profil of client"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Profil")

    phone_regex = RegexValidator(regex=r"^\+375\((25|29|33|44)\)\d{3}\-\d{2}-\d{2}$", message="Phone number must be +375(XX)XXX-XX-XX.")
    phone = models.CharField(validators=[phone_regex], max_length=17, verbose_name="Phone number")

    age = models.PositiveIntegerField(validators=[MinValueValidator(18, message="User must be older then 18")], verbose_name="Age")

    address = models.TextField(blank=True, verbose_name="Delivery address")

    def __str__(self):
        return f"{self.user.username} ({self.phone})"
    

class Order(models.Model):
    """Model of order"""

    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Client")
    books = models.ManyToManyField(Book, verbose_name="Books in order")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date of order")

    STATUS_CHOICE = {
        ('n', 'New'),
        ('p', 'In process'),
        ('d', 'Done'),
        ('c', 'Cancel')
    }

    status = models.CharField(max_length=1, choices=STATUS_CHOICE, default='n', verbose_name='Status of order')

    def __str__(self):
        return f"Order #{self.id} from {self.client.username}"

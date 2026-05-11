from django.db import models

# Create your models here.

class CompanyInfo(models.Model):

    name = models.CharField(max_length=200, verbose_name="Company name")
    description = models.TextField(verbose_name="Company description")
    history = models.TextField(verbose_name="History", blank=True)
    requisites = models.TextField(verbose_name="Details", blank=True)

    def __str__(self):
        return self.name
    
class Article(models.Model):
    """News"""

    title = models.CharField(max_length=100, verbose_name="Title of article")
    full_text = models.TextField(verbose_name="Text of article")
    image = models.ImageField(upload_to='news/', null=True, blank=True)
    publishing_date = models.DateField(auto_now_add=True, verbose_name="Date of publishing")

    def __str__(self):
        return self.title
    
class FAQ(models.Model):

    question = models.CharField(max_length=200, verbose_name="Question/Trem")
    answer = models.CharField(max_length=400, verbose_name="Answer")
    date = models.DateField(auto_now_add=True, verbose_name="Date of the last changing")

    def __str__(self):
        return self.question
class Employee(models.Model):
    full_name = models.CharField(max_length=150, verbose_name="Full- Last- Second name")
    position = models.CharField(max_length=100, verbose_name="Position in this company")
    email = models.EmailField(verbose_name="Email")
    photo = models.ImageField(upload_to='employees/', null=True, blank=True)

    def __str__(self):
        return self.full_name
    
class Vacancy(models.Model):
    title = models.CharField(max_length=100, verbose_name="Vacancy")
    description = models.CharField(max_length=1000, verbose_name="Description")

    def __str__(self):
        return self.title
    
class Review(models.Model):
    
    name = models.CharField(max_length=100)
    rating = models.PositiveIntegerField()
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
class PromoCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discode = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

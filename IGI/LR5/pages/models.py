from django.db import models
from django.contrib.auth.models import User

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

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    question = models.CharField(max_length=200, verbose_name="Question/Trem")
    answer = models.TextField(max_length=400, verbose_name="Answer", blank=True, null=True)
    date = models.DateField(auto_now_add=True, verbose_name="Date of the last changing")

    def __str__(self):
        return self.question
    
class Vacancy(models.Model):
    title = models.CharField(max_length=100, verbose_name="Vacancy")
    description = models.TextField(verbose_name="Description")

    def __str__(self):
        return self.title
    
class Review(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    name = models.CharField(max_length=100)
    rating = models.PositiveIntegerField()
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review from {self.name}"
    
class PromoCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discode = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

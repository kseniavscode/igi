from django.shortcuts import render
from .models import Book
# Create your views here.

def book_list(request):
    """Get all books from bd"""

    all_books = Book.objects.all()

    context = {
        'books': all_books
    }

    return render(request, 'store/book_list.html', context)
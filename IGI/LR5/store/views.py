from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Book
# Create your views here.

def book_list(request):
    """Get all books from bd and by searching"""

    search_query = request.GET.get('search', '')

    if search_query:
        books = Book.objects.filter(Q(authors__name__icontains=search_query) | Q(title__icontains=search_query) | Q(summery__icontains=search_query)).distinct()

    else:
        books = Book.objects.all()

    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }

    return render(request, 'store/book_list.html', context)

def book_details(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'store/book_details.html', {'book': book})
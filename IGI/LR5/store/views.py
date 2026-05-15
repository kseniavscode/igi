from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required
from .models import Book, BookInstance, Client, Order, Genre, Author, Language, Waitlist

from django.contrib.auth import login
from .forms import UserRegistrationForm

from django.utils import timezone
import statistics

from django.conf import settings

import requests
from django.core.files.base import ContentFile
import random

from django.contrib import messages
import re
# Create your views here.

@login_required
def import_books(request):

    if not hasattr(request.user, 'employee'):
        return redirect('book_list')
    
    search_results = []
    query = request.GET.get('q')

    if query:
        api_key = settings.GOOGLE_BOOKS_API_KEY
        url = f"https://www.googleapis.com/books/v1/volumes"

        params = {
            'q': query,
            'maxResults': 10,
            'key': api_key 
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])
            
            for item in items:

                isbn = None
                info = item.get('volumeInfo', {})

                publisher = info.get('publisher', 'Unknown Publisher')
                identifiers = info.get('industryIdentifiers', [])
                isbn = identifiers[0].get('identifier', '0000000000000') if identifiers else '0000000000000'

                if isbn and isbn != '0000000000000':
                    cover_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg?default=false"

                else:
                    image_link = info.get('imageLinks', {})
                    google_image = image_link.get('extraLarge', '') or image_link.get('large', '') or image_link.get('thumbnail', '')
                    cover_url = google_image.replace('zoom=1', 'zoom=4').replace('&edge=curl', '').replace('http://', 'https://')

                search_results.append({
                    'title': info.get('title'),
                    'authors': info.get('authors', ['Unknown Author']),
                    'description': info.get('description', 'No description available.'),
                    'categories': info.get('categories', ['General']),
                    'publisher': publisher,
                    'language': info.get('language', 'English'),
                    'cover_url': cover_url,
                    'isbn': isbn or '0000000000000'
                    
                    
                })

    if request.method == 'POST':

        title = request.POST.get('title')
        description = request.POST.get('description')
        isbn = request.POST.get('isbn')[:13]
        imprint = request.POST.get('publisher')
        lang_code = request.POST.get('language').upper()
        cover_url = request.POST.get('cover_url')

        lang_obj, _ = Language.objects.get_or_create(name=lang_code)


        new_book = Book.objects.create(
            title=title,
            summary=description,
            isbn=isbn,
            imprint=imprint,
            language=lang_obj,
            price=round(random.randint(20, 55), 2)
        )
        authors_list = request.POST.getlist('authors')
        for a_name in authors_list:
            author_obj, _ = Author.objects.get_or_create(name=a_name)
            new_book.authors.add(author_obj)

        categories_list = request.POST.getlist('categories')
        for c_name in categories_list:
            genre_obj, _ = Genre.objects.get_or_create(name=c_name)
            new_book.genre.add(genre_obj)

        stock_count = random.randint(5, 20)
        for _ in range(stock_count):
            BookInstance.objects.create(
                book=new_book,
                imprint=new_book.imprint,
                status='a'
            )
        if cover_url:
            cover_url = cover_url.replace('http://', 'https://')
            try:
                img_temp = requests.get(cover_url)
                if img_temp.status_code == 200:
                    file_name = f"{title.replace(' ', '_')[:20]}.jpg"
                    new_book.cover.save(file_name, ContentFile(img_temp.content), save=True)
            except:
                pass

        return redirect('book_list')
    
    return render(request, 'staff_panel/import_books.html', {'results': search_results, 'query': query})



def book_list(request):
    """Get all books from bd and by searching"""

    search_query = request.GET.get('search', '')

    if search_query:
        books = Book.objects.filter(Q(authors__name__icontains=search_query) | Q(title__icontains=search_query)).distinct()

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

    available_count = BookInstance.objects.filter(book=book, status='a').count()
    return render(request, 'store/book_details.html', {
        'book': book,
        'available_count': available_count
    })

@login_required
def update_book(request, pk):

    if not hasattr(request.user, 'employee'):
        return redirect('book_list')
    
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':

        title = request.POST.get('title').strip()
        cover = request.POST.get('cover')  
        imprint = request.POST.get('imprint').strip()
        isbn = request.POST.get('isbn').strip()
        price = request.POST.get('price')
        language = request.POST.get('language').strip()

        genres = request.POST.get('genres', '').strip()
        authors = request.POST.get('authors', '').strip()

        if not re.match(r'^[A-ZА-ЯЁa-zа-яё\,\s\.]+$', authors):
            messages.error(request, 'Enter rigth information about authors')
            return redirect('book_details', pk=book.pk)
        
        if not re.match(r'^[A-ZА-ЯЁa-zа-яё\,\s\.]+$', genres):
            messages.error(request, 'Enter rigth information about genres')
            return redirect('book_details', pk=book.pk)
        
        if not re.match(r'^[A-ZА-ЯЁa-zа-яё]+$', language):
            messages.error(request, 'Enter rigth information about language')
            return redirect('book_details', pk=book.pk)
        
        if not re.match(r'^\d+(\.\d{1,2})?$', price):
            messages.error(request, 'Enter rigth information about price')
            return redirect('book_details', pk=book.pk)
        
        if not re.match(r'^\d{13}$', isbn):
            messages.error(request, 'Enter rigth information about isbn')
            return redirect('book_details', pk=book.pk)
        
        if not re.match(r'^[A-ZА-ЯЁa-zа-яё]+([\s\-][A-ZА-ЯЁa-zа-яё]+)*$', imprint):
            messages.error(request, 'Enter rigth information about publishing house')
            return redirect('book_details', pk=book.pk)
        
        if not re.match(r'^[\d\s\`\-\:\!\?\.A-ZА-ЯЁa-zа-яё]+$', title):
            messages.error(request, 'Enter rigth information about a book`s title')
            return redirect('book_details', pk=book.pk)
        
        book.title = title
        book.summary = request.POST.get('summary')
        book.isbn = isbn
        book.imprint = imprint
        book.price = price

        lang, _ = Language.objects.get_or_create(name=language)
        book.language = lang

        a = [i.strip() for i in authors.split(',') if i.strip()]
        book.authors.clear()
        for author in a:
            aut, _ = Author.objects.get_or_create(name=author)
            book.authors.add(aut)

        g = [i.strip() for i in genres.split(',') if i.strip()]
        book.genre.clear()
        for genre in g:
            gen, _ = Genre.objects.get_or_create(name=genre)
            book.genre.add(gen)

        if 'cover' in request.FILES:
            book.cover = request.FILES['cover']

        book.save()
        messages.success(request, 'Success: Data is updated')
    return redirect('book_details', pk=book.pk)

@login_required
def delete_book(request, pk):

    if not hasattr(request.user, 'employee'):
        return redirect('book_list')
    
    book = get_object_or_404(Book, pk=pk)
    BookInstance.objects.filter(book=book).delete()
    book.delete()
    return redirect('book_list')

@login_required
def add_to_orders(request, pk):
    book = get_object_or_404(Book, pk=pk)
    client = get_object_or_404(Client, user=request.user)
    
    book_instance = BookInstance.objects.filter(book=book, status='a').first()

    if book_instance:
        order, _ = Order.objects.get_or_create(client=client, status='n')
        
        book_instance.status = 'r'
        book_instance.order = order
        book_instance.save()

        order.books.add(book)
        return redirect('my_orders')
    else:
        Waitlist.objects.get_or_create(client=client, book=book)
        return redirect('book_details', pk=pk)

@login_required
def my_orders(request):
    client = get_object_or_404(Client, user=request.user)
    orders = Order.objects.filter(client=client).exclude(status='c').order_by('-created_at')
    return render(request, 'store/my_orders.html', {'orders': orders})
@login_required
def confirm_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.status == 'n':
        order.status = 'p'
        order.updated_at = timezone.now()
        order.save()
    return redirect('my_orders')

@login_required
def cancel_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.status == 'n':

        instances = BookInstance.objects.filter(order=order)
        for ins in instances:
            ins.status = 'a'
            ins.order = None
            ins.save()

        order.status = 'c'
        order.save()
    return redirect('my_orders')

@login_required
def order_management(request):

    if not hasattr(request.user, 'employee'):
        return redirect('book_list')
    
    search_query = request.GET.get('search', '')

    orders = Order.objects.filter(status='p').order_by('-created_at')

    if search_query:
        orders = orders.filter(Q(client__user__username__icontains=search_query) | Q(client__phone__icontains=search_query))

    total_revenue = Order.objects.filter(status='d').aggregate(total=Sum('instances__book__price'))['total'] or 0

    count_done_orders = Order.objects.filter(status='d').count()

    content = {
        'orders': orders,
        'total_revenue': total_revenue,
        'count_done_orders': count_done_orders,
        'search_query': search_query,
    }
    return render(request, 'staff_panel/order_management.html', content)

@login_required
def complete_order(request, pk):

    if not hasattr(request.user, 'employee'):
        return redirect('book_list')
    
    order = get_object_or_404(Order, pk=pk)
    if order.status == 'p': 

        instances = BookInstance.objects.filter(order=order)

        for ins in instances:
            ins.status = 's'
            ins.save()

        order.status = 'd'  
        order.save()
    return redirect('order_management')

@login_required
def statistic_view(request):

    if not hasattr(request.user, 'employee'):
        return redirect('book_list')
    
    context = {}

    clients_alphabetical = Client.objects.order_by('user__username')
    books_alphabetical = Book.objects.order_by('title')

    done_orders = Order.objects.filter(status='d')
    total_revenue = done_orders.aggregate(total=Sum('instances__book__price'))['total'] or 0

    order_total = [o.total_price() for o in done_orders]

    if order_total:
        revenue_mean = statistics.mean(order_total)
        revenue_median = statistics.median(order_total)

        try:
            revenue_mode = statistics.mode(order_total)
        except statistics.StatisticsError:
            revenue_mode = 'Multiple modes'
    else:
        revenue_mean = revenue_median = revenue_mode = 0


    ages = [c.get_age() for c in Client.objects.all()]
    if ages:
        age_mean = statistics.mean(ages)
        age_median = statistics.median(ages)
    else:
        age_mean = age_median = 0

    popular_genre = Genre.objects.filter(book__bookinstance__order__status='d').annotate(profit=Count('book__bookinstance')).order_by('-profit').first()
    profitable_genre = Genre.objects.filter(book__bookinstance__order__status='d').annotate(profit=Sum('book__bookinstance__book__price')).order_by('-profit').first()
    

    context.update({
        'clients': clients_alphabetical,
        'books': books_alphabetical,
        'total_revenue': total_revenue,
        'revenue_mean': revenue_mean,
        'revenue_median': revenue_median,
        'revenue_mode': revenue_mode,
        'age_mean': age_mean,
        'age_median': age_median,
        'popular_genre': popular_genre,
        'profitable_genre': profitable_genre,
    })

    top_book = Book.objects.annotate(sales_count=Count('order', filter=Q(bookinstance__order__status='d'))).order_by('sales_count').first()
    loser_book = Book.objects.annotate(sales_count=Count('order', filter=Q(bookinstance__order__status='d'))).order_by('-sales_count').first()

    context.update({
        'top_book': top_book,
        'loser_book': loser_book,
    })

    monthly_sales_data = Order.objects.filter(status='d').annotate(month=TruncMonth('updated_at')).values('month').annotate(total=Sum('instances__book__price')).order_by('month')

    chart_labels = [data['month'].strftime("%b %Y") for data in monthly_sales_data]
    chart_data = [float(data['total']) for data in monthly_sales_data]

    context.update({
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    })

    y_values = chart_data
    n = len(y_values)
    x_values = list(range(1, n + 1))

    if n > 1:
        sum_x = sum(x_values)
        sum_y = sum(y_values)
        sum_xy = sum(x * y for x, y in zip(x_values, y_values))
        sum_xx = sum(x * x for x in x_values)

        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x**2)
        intercept = (sum_y - slope * sum_x) / n
        
        trend_line_data = [round(slope * x + intercept, 2) for x in x_values]

        next_month = n+1
        forecast_value = round(slope * next_month + intercept, 2)

    else:
        trend_line_data = []
        forecast_value = 0

    context.update({
        'trend_line_data': trend_line_data,
        'forecast_value': forecast_value,
    })

    raw_report_data = Genre.objects.filter(book__bookinstance__order__status= 'd').annotate(month=TruncMonth('book__bookinstance__order__updated_at')).values('name', 'month').annotate(total=Sum('book__bookinstance__book__price')).order_by('name', 'month')

    report_months = sorted(list(set(row['month'] for row in raw_report_data if row['month'] )))
    table_headers = [m.strftime("%b %Y") for m in report_months]

    annual_report = {}

    for row in raw_report_data:
        genre_name = row['name']
        month_date = row['month']
        profit = float(row['total'] or 0)

        if genre_name not in annual_report:
            annual_report[genre_name] = {m: 0.0 for m in report_months}

        annual_report[genre_name][month_date] = profit

    context.update({
        'table_headers': table_headers,
        'annual_report': annual_report,
    })

    return render(request, 'staff_panel/stats.html', context)

@login_required
def manage_stock(request):
    if not hasattr(request.user, 'employee'):
        return redirect('book_list')
    
    books = Book.objects.annotate(in_stock=Count('bookinstance', filter=Q(bookinstance__status='a'), distinct=True),
                                  waiting=Count('waitlist', distinct=True)).order_by('title')
    search_query = request.GET.get('search', '')

    if search_query:
        books = books.filter(Q(title__icontains=search_query)).distinct()

    
    return render(request, 'staff_panel/manage_stock.html', {
        'books': books,
        'search_query': search_query
    })

@login_required
def add_instance(request, pk):
    if not hasattr(request.user, 'employee'):
        return redirect('book_list')
    
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        count = int(request.POST.get('count', 1))

        for _ in range(count):
            new_instance = BookInstance.objects.create(
                book=book,
                imprint=book.imprint,
                status='a'
            )

            waiting_user = Waitlist.objects.filter(book=book).order_by('added_at').first()

            if waiting_user:

                order, _ = Order.objects.get_or_create(client=waiting_user.client, status='n')
                new_instance.status = 'r'
                new_instance.order = order
                new_instance.save()

                order.books.add(book)

                waiting_user.delete()

        return redirect('manage_stock')




def register(request):
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            Client.objects.create(
                user=user,
                phone=form.cleaned_data['phone'],
                birth_date=form.cleaned_data['birth_date'],
                address=form.cleaned_data['address']
            )

            login(request, user)
            return redirect('book_list')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Avg, Count
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required
from .models import Book, Client, Order, Genre

from django.contrib.auth import login
from .forms import UserRegistrationForm

from django.utils import timezone
import statistics
# Create your views here.

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
    return render(request, 'store/book_details.html', {'book': book})


@login_required
def add_to_orders(request, pk):
    book = get_object_or_404(Book, pk=pk)
    client = get_object_or_404(Client, user=request.user)
    
    order, created = Order.objects.get_or_create(client=client, status='n')
    order.books.add(book)
    
    return redirect('my_orders')

@login_required
def my_orders(request):
    client = get_object_or_404(Client, user=request.user)
    orders = Order.objects.filter(client=client).order_by('-created_at')
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

    total_revenue = Order.objects.filter(status='d').aggregate(total=Sum('books__price'))['total'] or 0

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
    total_revenue = done_orders.aggregate(total=Sum('books__price'))['total'] or 0

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


    ages = Client.objects.values_list('age', flat=True)
    if ages:
        age_mean = statistics.mean(ages)
        age_median = statistics.median(ages)
    else:
        age_mean = age_median = 0

    popular_genre = Genre.objects.annotate(profit=Count('book__order', filter=Q(book__order__status='d'))).order_by('-profit').first()
    profitable_genre = Genre.objects.annotate(profit=Count('book__price', filter=Q(book__order__status='d'))).order_by('-profit').first()
    

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

    top_book = Book.objects.annotate(sales_count=Count('order', filter=Q(order__status='d'))).order_by('sales_count').first()
    loser_book = Book.objects.annotate(sales_count=Count('order', filter=Q(order__status='d'))).order_by('-sales_count').first()

    context.update({
        'top_book': top_book,
        'loser_book': loser_book,
    })

    monthly_sales_data = Order.objects.filter(status='d').annotate(month=TruncMonth('updated_at')).values('month').annotate(total=Sum('books__price')).order_by('month')

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

    raw_report_data = Genre.objects.filter(book__order__status= 'd').annotate(month=TruncMonth('book__order__updated_at')).values('name', 'month').annotate(total=Sum('book__price')).order_by('name', 'month')

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
                age=form.cleaned_data['age'],
                address=form.cleaned_data['address']
            )

            login(request, user)
            return redirect('book_list')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})
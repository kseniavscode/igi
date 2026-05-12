from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.contrib.auth.decorators import login_required
from .models import Book, Client, Order

from django.contrib.auth import login
from .forms import UserRegistrationForm

from django.utils import timezone
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

def sales_stats(request):
    total_sales = Order.objects.filter(status='d').aggregate(Sum('books__price'))['books__price__sum'] or 0
    
    orders_count = Order.objects.count()
    
    return render(request, 'store/stats.html', {
        'total_sales': total_sales,
        'orders_count': orders_count
    })






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
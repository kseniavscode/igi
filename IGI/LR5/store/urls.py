from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_details, name='book_details'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='book_list'), name='logout'),

    path('add-to-orders/<int:pk>/', views.add_to_orders, name='add_to_orders'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order/confirm/<int:pk>/', views.confirm_order, name='confirm_order'),
    path('order/cancel/<int:pk>', views.cancel_order, name='cancel_order'),
    path('order/complete/<int:pk>', views.complete_order, name='complete_order'),

    path('order-management/', views.order_management, name='order_management'),
    path('stats/', views.statistic_view, name='stats'),
    path('import_books/', views.import_books, name='import_books'),
    path('manage_stock/', views.manage_stock, name='manage_stock'),
    path('add_instance/<int:pk>/', views.add_instance, name='add_instance'),
    
]
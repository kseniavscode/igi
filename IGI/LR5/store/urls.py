from django.urls import re_path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    re_path(r'^$', views.book_list, name='book_list'),
    re_path(r'^book/(?P<pk>\d+)/$', views.book_details, name='book_details'),
    re_path(r'^register/$', views.register, name='register'),
    re_path(r'^login/$', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(next_page='book_list'), name='logout'),

    re_path(r'^add-to-orders/(?P<pk>\d+)/$', views.add_to_orders, name='add_to_orders'),
    re_path(r'^my-orders/$', views.my_orders, name='my_orders'),
    re_path(r'^order/confirm/(?P<pk>\d+)/$', views.confirm_order, name='confirm_order'),
    re_path(r'^order/cancel/(?P<pk>\d+)/$', views.cancel_order, name='cancel_order'),
    re_path(r'^order/complete/(?P<pk>\d+)/$', views.complete_order, name='complete_order'),

    re_path(r'^order-management/$', views.order_management, name='order_management'),
    re_path(r'^stats/$', views.statistic_view, name='stats'),
    re_path(r'^import_books/$', views.import_books, name='import_books'),
    re_path(r'^manage_stock/$', views.manage_stock, name='manage_stock'),
    re_path(r'^add_instance/(?P<pk>\d+)/$', views.add_instance, name='add_instance'),

    re_path(r'^book/(?P<pk>\d+)/update/$', views.update_book, name='update_book'),
    re_path(r'^book/(?P<pk>\d+)/delete/$', views.delete_book, name='delete_book'),

    re_path(r'^point/$', views.pickup_points_view, name='points'),

    
]
from django.contrib import admin

from .models import Author, Genre, Language, Book, BookInstance, Client, Employee, Order

# Register your models here.
class OrderInline(admin.TabularInline):
    model = Order
    extra = 0

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'age')
    inlines = [OrderInline]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'created_at', 'updated_at', 'status')
    list_editable = ('updated_at', 'status')
    list_filter = ('status', 'created_at', 'updated_at')
    filter_horizontal = ('books',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'user', 'email')
    search_fields = ('full_name', 'position', 'email')
    list_filter = ('position',)

admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Book)
admin.site.register(BookInstance)

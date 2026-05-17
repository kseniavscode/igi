from django.contrib import admin

from .models import Author, Genre, Language, Book, BookInstance, Client, Employee, Order, Waitlist, PickupPoint

# Register your models here.
class OrderInline(admin.TabularInline):
    model = Order
    extra = 0

class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0
    readonly_fields = ('id',)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'phone', 'birth_date')
    list_filter = ('city',)
    inlines = [OrderInline]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'created_at', 'updated_at', 'status')
    list_editable = ('updated_at', 'status')
    list_filter = ('status', 'created_at', 'updated_at')
    filter_horizontal = ('books',)
    inlines = [BookInstanceInline]

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'user', 'email')
    search_fields = ('full_name', 'position', 'email')
    list_filter = ('position',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_authors', 'price', 'language', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'genre')
    filter_horizontal = ('authors', 'genre')
    search_fields = ('title', 'isbn', 'author__last_name')

    def get_authors(self, obj):
        return ", ".join([a.name for a in obj.authors.all()])
    get_authors.short_description = 'Authors'

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    
    search_fields = ('id', 'book__title')

@admin.register(Waitlist)
class WaitlistAdmin(admin.ModelAdmin):
    list_display = ('client', 'book', 'added_at')
    list_filter = ('added_at',)

admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(PickupPoint)
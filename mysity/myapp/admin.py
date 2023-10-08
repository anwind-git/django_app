from django.contrib import admin
from .models import Products, MenuCategories, Orders, OrderItem, UserProfile
from django.utils.safestring import mark_safe

admin.site.site_header = "Панель администратора"
admin.site.site_title = "Панель администрирования"
admin.site.index_title = "Добро пожаловать в админку"

@admin.register(Products)
class ProductstAdmin(admin.ModelAdmin):

    list_display = ['product_name', 'get_html_photo', 'price', 'time_update', 'publication']
    search_fields = ['product_name', 'description', 'price']
    list_per_page = 15
    list_filter = ['menu_categories', 'publication', 'time_create']
    filter_horizontal = ['menu_categories']
    fields = ['product_name', 'slug', 'description', 'image', 'get_html_photo',
              'price', 'menu_categories', 'product_quantity', 'time_create', 'time_update', 'publication']
    readonly_fields = ['get_html_photo', 'time_create', 'time_update']
    list_editable = ['publication']
    prepopulated_fields = {'slug': ('product_name',)}

    def get_html_photo(self, obj):
        if obj.image:
            return mark_safe(f"<img src={obj.image.url} width=50>")

    get_html_photo.short_description = "Миниатюра"


@admin.register(MenuCategories)
class MenuCategoriesAdmin(admin.ModelAdmin):
    list_display = ['categorie', 'slug', 'queue']
    list_per_page = 15
    prepopulated_fields = {'slug': ('categorie',)}


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Orders)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'created', 'paid', 'delivered']
    list_filter = ['paid', 'created', 'delivered']
    inlines = [OrderItemInline]
    list_per_page = 15


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_per_page = 15
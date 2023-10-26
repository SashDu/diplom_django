from django.contrib import admin
from .models import *

# # Аналогичный (упрощенный) способ:
# admin.site.register(User)
# admin.site.register(Company)
# admin.site.register(Country)
# admin.site.register(Side)
# admin.site.register(GroupProduct)
# admin.site.register(Product)
# admin.site.register(Articles)
# admin.site.register(Feedback)


# Регистрация и настройка модели User
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username"]

    # Для дополнительного отображения модели Basket в модели User
    class BasketAdmin(admin.TabularInline):
        model = Basket
        fields = ('product', 'quantity', 'created_timestamp')
        readonly_fields = ('created_timestamp',)  # только для чтения
        extra = 0  # для скрытия дополнительных пустых полей, идущих по умолчанию
    # Для отображения дополнительного поля с Корзиной
    inlines = [BasketAdmin]


# Регистрация и настройка модели Company
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    # Пагинация в админке (При отображении модели)
    list_per_page = 3
    # Отображение поискового поля
    search_fields = ['__str__']


# Регистрация и настройка модели Country
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    # Отображение поискового поля
    search_fields = ['name']


# Регистрация и настройка модели Side
@admin.register(Side)
class SideAdmin(admin.ModelAdmin):
    # Порядок вывода СТОЛБИКОВ (При отображении модели)
    list_display = ["side"]


# Регистрация и настройка модели GroupProduct
@admin.register(GroupProduct)
class GroupProductAdmin(admin.ModelAdmin):
    # Порядок вывода СТОЛБИКОВ (При отображении модели)
    list_display = ['view']
    # prepopulated_fields = {'slug': ('view',)}


# Регистрация и настройка модели Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Порядок вывода СТОЛБИКОВ (При отображении модели)
    list_display = ['title', 'company', 'category', 'side', 'price', 'product_code']
    # # Возможность корректировки СТОЛБИКОВ (первый столбик убираем, поскольку он должен быть кликабелен)
    list_editable = ['price']
    # Пагинация в админке (При отображении модели)
    list_per_page = 3
    # Отображение поискового поля
    search_fields = ['title', 'price']
    # Добавление ФИЛЬТРА (По перечисленным полям)
    list_filter = ['title', 'company', 'category', 'price']
    # Порядок вывода ПОЛЕЙ (При заполнении модели)
    fieldsets = (("Основное", {"fields": ('title', 'company', 'price', 'category', 'side')}),
                 ("Дополнительное", {"fields": ("manufacturer", "summary", "product_code", "quantity", "image")}))
    # prepopulated_fields = {'slug': ('title',)}


# Регистрация и настройка модели Articles
@admin.register(Articles)
class ArticlesAdmin(admin.ModelAdmin):
    pass


# Регистрация и настройка модели Feedback
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    # Порядок вывода СТОЛБИКОВ (При отображении модели)
    list_display = ["name", 'email', 'phoneNumber']
    # Отображение поискового поля
    search_fields = ['name', 'phoneNumber']
    # Добавление ФИЛЬТРА (По перечисленным полям)
    list_filter = ['name', 'phoneNumber']


# Регистрация и настройка модели EmailVerification
@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ['code', 'user', 'expiration']
    fields = ['code', 'user', 'expiration', 'created']
    readonly_fields = ['created']


# Регистрация и настройка модели Order
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status')
    fields = (
        'id', 'created',
        ('first_name', 'last_name'),
        ('email', 'address'),
        'basket_history', 'status', 'initiator',
    )
    readonly_fields = ('id', 'created')

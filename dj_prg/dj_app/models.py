from django.db import models
from django.contrib.auth.models import AbstractUser  # Импортируем встроенную модель "Пользователи"
from django.core.validators import RegexValidator  # Для сохранения номера телефона
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.timezone import now
# from phonenumber_field.modelfields import PhoneNumberField  # Для номера телефона с префиксом
# Модель User (для создания страницы с профилем)


class User(AbstractUser):
    image = models.ImageField(
        upload_to='user_img',
        null=True,
        blank=True,
        verbose_name="Добавить изображение"
    )
    is_verified_email = models.BooleanField(default=False)


# Модель Компания (Company)
class Company(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name="Название компании"
    )
    objects = models.Model

    # При просмотре всей модели из админки (поле которое будет отображаться в таблице)
    def __str__(self):
        return self.name

    # НАСТРОЙКИ перевода модели и сортировки объектов на главной таблице
    class Meta:
        verbose_name = "Компанию"  # Название модели в ед.числе
        verbose_name_plural = "Компании"  # Название модели в мнж.числе
        ordering = ["name"]  # Сортировка по полю (если с "-" то в обратном порядке)


# Модель Страна (Country)
class Country(models.Model):
    name = models.CharField(max_length=20, verbose_name="Страна")
    objects = models.Model

    # При просмотре всей модели из админки (поле которое будет отображаться в таблице)
    def __str__(self):
        return self.name

    # НАСТРОЙКИ перевода модели и сортировки объектов на главной таблице
    class Meta:
        verbose_name = "Страна"  # Название модели в ед.числе
        verbose_name_plural = "Страны"  # Название модели в мнж.числе
        ordering = ["name"]  # Сортировка по полю (если с "-" то в обратном порядке)


# Модель Сторона (Side)
class Side(models.Model):
    side = models.CharField(
        max_length=20,
        help_text="Введите сторону",
        verbose_name="Сторона"
    )
    objects = models.Model

    # При просмотре всей модели из админки (поле которое будет отображаться в таблице)
    def __str__(self):
        return self.side

    # НАСТРОЙКИ перевода модели и сортировки объектов на главной таблице
    class Meta:
        verbose_name = "Сторона"  # Название модели в ед.числе
        verbose_name_plural = "Стороны"  # Название модели в мнж.числе
        ordering = ["side"]  # Сортировка по полю (если с "-" то в обратном порядке)


# Модель Группа (GroupProduct)
class GroupProduct(models.Model):
    view = models.CharField(
        max_length=30,
        unique=True,
        help_text="Введите вид товара",
        verbose_name="Вид товара"
    )
    slug = models.SlugField(max_length=200, blank=True)
    objects = models.Model

    # При просмотре всей модели из админки (поле которое будет отображаться в таблице)
    def __str__(self):
        return self.view

    # НАСТРОЙКИ перевода модели и сортировки объектов на главной таблице
    class Meta:
        verbose_name = "Категория товара"  # Название модели в ед.числе
        verbose_name_plural = "Категории товаров"  # Название модели в мнж.числе
        ordering = ["view"]  # Сортировка по полю (если с "-" то в обратном порядке)


# Модель Продукт
class Product(models.Model):
    company = models.ForeignKey(Company, null=True,
                                on_delete=models.CASCADE,
                                help_text="Выберите ,бренд",
                                verbose_name="Бренд")  # Связывающее поле
    slug = models.SlugField(
        max_length=200,
        db_index=True,
        blank=True,
        verbose_name="url"
    )
    title = models.CharField(
        max_length=200,
        help_text="Введите название товара",
        verbose_name="Название товара"
    )
    summary = models.TextField(
        max_length=1000,
        help_text="Введите описание товара",
        verbose_name="Описание товара"
    )
    product_code = models.IntegerField(
        null=True,
        help_text="Введите код товара",
        verbose_name="Код товара"
    )
    manufacturer = models.ForeignKey(Country,
                                     null=True,
                                     on_delete=models.CASCADE,
                                     max_length=20,
                                     help_text="Введите страну производителя",
                                     verbose_name="Страна производителя"
                                     )
    price = models.DecimalField(
        null=True,
        max_digits=5,
        decimal_places=2,
        help_text="Введите цену товара",
        verbose_name="Цена товара"
    )
    quantity = models.PositiveIntegerField(
        default=0,
        help_text="Введите количество товара",
        verbose_name="Количество товара"
    )
    # НУЖНО СМЕНИТЬ НАЗВАНИЕ КАТЕГОРИИ (ВИДА) ТОВАРА ВО ИЗБЕЖАНИЕ ПУТАНИЦЫ ПЕРЕД СЛЕД. МИГРАЦИЕЙ \ DONE
    category = models.ForeignKey(GroupProduct,
                                 related_name='products',
                                 null=True, on_delete=models.CASCADE,
                                 help_text="Выберите вид (категорию) товара",
                                 verbose_name="Вид (категория) товара"
                                 )
    side = models.ForeignKey(Side, null=True,
                             on_delete=models.CASCADE,
                             help_text="Выберите категорию",
                             verbose_name="Категория"
                             )
    image = models.ImageField(
        upload_to='products/%Y/%m/%d',
        null=True, blank=True,
        verbose_name="Добавить изображение"
    )
    available = models.BooleanField(default=True)
    objects = models.Model

    # При просмотре всей модели из админки (поле которое будет отображаться в таблице)
    def __str__(self):
        return self.title

    # [ВНУТРЕННИЙ МЕТОД] Возвращающий ссылку на товар
    def get_absolute_url(self):
        return f'/product/{self.pk}'

    # НАСТРОЙКИ перевода модели и сортировки объектов на главной таблице
    class Meta:
        verbose_name = "Продукт"  # Название модели в ед.числе
        verbose_name_plural = "Продукты"  # Название модели в мнж.числе
        ordering = ["title"]  # Сортировка по полю (если с "-" то в обратном порядке)
        index_together = (('id', 'slug'),)


# Дополнительный менеджер к модели Корзина
class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)

    def stripe_products(self):
        line_items = []
        for basket in self:
            item = {
                'price': basket.product.stripe_product_price_id,
                'quantity': basket.quantity,
            }
            line_items.append(item)
        return line_items


# Модель Корзина
class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name="Количество")
    created_timestamp = models.DateTimeField(auto_now_add=True)
    # objects = models.Model
    # переопределение стандартного objects в классе BasketQuerySet
    objects = BasketQuerySet.as_manager()

    # При просмотре всей модели из админки (поле которое будет отображаться в таблице)
    def __str__(self):
        return f'Корзина для {self.user} | Продукт: {self.product.title}'

    def sum(self):
        return self.product.price * self.quantity

    # НАСТРОЙКИ перевода модели и сортировки объектов на главной таблице
    class Meta:
        verbose_name = "Корзина"  # Название модели в ед.числе
        verbose_name_plural = "Корзины"  # Название модели в мнж.числе
        ordering = ["product"]  # Сортировка по полю (если с "-" то в обратном порядке)


# Модель Заказ
class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUSES = (
        (CREATED, 'Создан'),
        (PAID, 'Оплачен'),
        (ON_WAY, 'В пути'),
        (DELIVERED, 'Доставлен'),
    )

    first_name = models.CharField(
        max_length=64,
        verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=64,
        verbose_name="Фамилия"
    )
    email = models.EmailField(
        max_length=256,
        verbose_name="Почтовый ящик"
    )
    address = models.CharField(
        max_length=256,
        verbose_name="Адрес доставки"
    )
    basket_history = models.JSONField(
        default=dict,
        verbose_name="История корзины"
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создано"
    )
    status = models.SmallIntegerField(
        default=CREATED,
        choices=STATUSES,
        verbose_name="Статус"
    )
    initiator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Заказчик")

    def __str__(self):
        return f'Order #{self.id}. {self.first_name} {self.last_name}'

        # НАСТРОЙКИ перевода модели и сортировки объектов на главной таблице

    class Meta:
        verbose_name = "Заказ"  # Название модели в ед.числе
        verbose_name_plural = "Заказы"  # Название модели в мнж.числе
        ordering = ["created"]  # Сортировка по полю (если с "-" то в обратном порядке)


# Модель Статьи

class Articles(models.Model):
    title = models.CharField(
        max_length=30,
        verbose_name="Заголовок статьи"
    )
    anons = models.CharField(
        max_length=250,
        verbose_name="Анонс статьи"
    )
    summary = models.TextField(
        max_length=2000,
        verbose_name="Описание"
    )
    date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата публикации"
    )
    image = models.ImageField(
        upload_to='articles/%Y/%m/%d',
        null=True,
        blank=True,
        verbose_name="Добавить изображение"
    )
    objects = models.Model

    # При просмотре всей модели из админки (поле которое будет отображаться в таблице)
    def __str__(self):
        return self.title

    # [ВНУТРЕННИЙ МЕТОД] Возвращающий ссылку на статью
    def get_absolute_url(self):
        return f'/article/{self.pk}'
        # return "/article/{}".format(self.pk)  # то же самое
        # !!! На будущее лучше называть модели в ед. числе, чтобы не было потом путаницы !!!

    # НАСТРОЙКИ перевода модели и сортировки объектов на главной таблице
    class Meta:
        verbose_name = "Статью"  # Название модели в ед.числе
        verbose_name_plural = "Статьи"  # Название модели в мнж.числе
        ordering = ["-date"]  # Сортировка по полю (если с "-" то в обратном порядке)


# Модель Обратная связь
class Feedback(models.Model):
    name = models.CharField(
        null=True,
        max_length=10,
        verbose_name="Имя"
    )
    email = models.EmailField(verbose_name="Email")
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phoneNumber = models.CharField(
        validators=[phoneNumberRegex],
        max_length=16,
        unique=False
    )
    # phone = PhoneNumberField()  # для способа с префиксом (нужна доработка)
    message = models.TextField(
        max_length=200,
        verbose_name="Текст сообщения"
    )
    objects = models.Model

    # При просмотре всей модели из админки (поле которое будет отображаться в таблице)
    def __str__(self):
        return self.name

    # НАСТРОЙКИ перевода модели и сортировки объектов на главной таблице
    class Meta:
        verbose_name = "Обращение"  # Название модели в ед.числе
        verbose_name_plural = "Обращения"  # Название модели в мнж.числе
        ordering = ["-email"]  # Сортировка по полю (если с "-" то в обратном порядке)


# Модель верификации почтового ящика
class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()
    objects = models.Model

    def __str__(self):
        return f'EmailVerification object for {self.user.email}'

    def send_verification_email(self):
        link = reverse('email_verification', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подтверждение учетной записи для {self.user.username}'
        message = 'Для подтверждения учетной записи {} перейдите по ссылке: {}'.format(
            self.user.email,
            verification_link
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    # Метод на проверку просрочена ли ссылка или нет
    def is_expired(self):
        return True if now() >= self.expiration else False

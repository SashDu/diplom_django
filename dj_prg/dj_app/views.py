from django.contrib.auth.decorators import login_required  # Для перенаправления гостя на авторизацию
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .forms import *
from .models import *
from rank import Rating  # использование парсинга
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView  # Для входа/выхода
from django.db.utils import IntegrityError  # Импорт ошибки при регистрации
from django.core.mail import EmailMultiAlternatives  # Импорт для боевой отправки по почте
from django.template.loader import render_to_string  # Импорт для боевой отправки по почте
from django.urls import reverse, reverse_lazy  # Для правильного перехода после отправки формы


# Метод Главной страницы сайта
class IndexView(TemplateView):
    template_name = 'index.html'


# Метод Входа(Авторизации)/Выхода
class LoginUser(LoginView):
    form_class = Login
    template_name = "registration/login.html"


# Метод Формы регистрации
class Registration(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('login')  # альтернатива перенаправления, описанного в html


# Метод страницы Профиль
@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            print("Успешно")
            return HttpResponseRedirect(reverse('profile'))
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=request.user)
    context = {"form": form}
    return render(request, "registration/profile.html", context=context)


# Метод страницы О нас
def about(request):
    year = 2015
    workers = 50
    companies = "BOSCH, TYC, DEPO, HELLA, VALEO"
    context = {"year": year, "workers": workers, "companies": companies}
    return render(request, "about.html", context=context)


# Метод страницы Контакты + Обратная связь
def contacts(request):
    if request.method == "GET":
        form = FeedbackForm()  # Создание формы
        context = {"form": form}  # Генерация context
        return render(request, "contacts.html", context=context)  # Показываем шаблон
    if request.method == "POST":
        # Получаем данные из формы
        name = request.POST.get("name")
        email = request.POST.get("email")
        phoneNumber = request.POST.get("phoneNumber")
        message = request.POST.get("message")
        try:
            if not name == "" and not email == "" and not phoneNumber == "" and not message == "":
                kwargs = {"name": name, "email": email, "phoneNumber": phoneNumber, "message": message}  # Передаваемые аргументы
                DataBase.write(model=Feedback, **kwargs)  # Запись в БД
            # return redirect("contacts")  # альтернативный вариант без уведомления пользователя
            DataBase.read(model=Feedback)  # Читаю таблицу
            context = {"name": name}  # Генерация context
            return render(request, "contacts.html", context=context)  # Показываем шаблон
        except IntegrityError:
            context = {"error": name}  # Генерация context
            return render(request, "contacts.html", context=context)


# Метод страницы Рейтинг
def rating(request):
    obj_rating = Rating
    table_rating = obj_rating.get_rows()  # исходные данные рейтинга
    data = [[row[i] for row in table_rating]
            for i in range(len(table_rating[0]))]  # преобразование данных из table_rating в новые списки
    context = {"table_rating": data}  # , "my_loop": [0] (для второго способа)
    return render(request, "rating.html", context=context)


# Метод страницы Соглашение
class Agreement(TemplateView):
    template_name = 'agreement.html'


# Метод страницы Корзина
def basket(request):
    baskets = Basket.objects.filter(user=request.user)  # забираю нужные значения по корзине из модели
    total_sum = 0
    total_quantity = 0
    for basket in baskets:
        total_sum += basket.sum()
        total_quantity += basket.quantity
    context = {"baskets": baskets, "total_sum": total_sum, "total_quantity": total_quantity}
    return render(request, "basket.html", context=context)


# Метод Добавления товара в корзину
# декоратор @login_required используется для отправки на авторизацию
@login_required
def add_basket(request, product_id):
    product = Product.objects.get(id=product_id)  # забираю все данные по продукту
    baskets = Basket.objects.filter(user=request.user, product=product)  # передаю в корзину данные по продукту и юзеру
    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])  # возврат на ту же страницу


# Метод Добавления товара в корзину
@login_required
def delete_basket(request, basket_id):
    basket = Basket.objects.get(id=basket_id)  # забираю все данные по продуктам в корзине
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])  # возврат на ту же страницу


class ArticlesListView(ListView):
    model = Articles  # Модель читаемая для шаблона
    paginate_by = 3  # Сколько объектов будет передано в шаблон


class ArticlesDetailView(DetailView):
    model = Articles


# Метод добавления статей (Автоматически генерируется при помощи CreateView)
# Шаблон: "templates/dj_app/articles_form.html"
class ArticlesCreate(CreateView):
    model = Articles
    form_class = ArticlesForm
    # fields = "__all__"  # все поля по умолчанию
    success_url = reverse_lazy("articles")  # Адрес перенаправления на список всех книг (после успешной отправки формы)


# Метод обновления статьи (Автоматически генерируется при помощи UpdateView)
# Шаблон: "templates/dj_app/articles_form.html"
class ArticlesUpdateView(UpdateView):
    model = Articles
    form_class = ArticlesForm
    # template_name = "dj_app/articles_form.html"  # задаётся если вдруг нужен другой шаблон
    # fields = ["title", "anons", "summary", "date", "image"]  # для стандартного отображения полей либо = "__all__"


# Метод удаления статьи (Автоматически генерируется при помощи DeleteView)
# Шаблон: "templates/dj_app/articles_confirm_delete.html"
class ArticlesDeleteView(DeleteView):
    model = Articles
    success_url = '/articles'


# Список всех статей (Автоматически генерируется при помощи ListView)
# Шаблон: "templates/dj_app/product_list.html"
# Переменная (шаблона/ключ): "product_list", такое название присваивается по умолчанию
class ProductListView(ListView):
    model = Product  # Модель читаемая для шаблона
    paginate_by = 6  # Сколько объектов будет передано в шаблон

    # Фильтруем по нужным категориям товаров
    def get_queryset(self):
        queryset = super(ProductListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    # Отбираем и показываем нужный context
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data()
        context['categories'] = GroupProduct.objects.all()
        return context


# Конкретная статья (Автоматически генерируется при помощи DetailView)
# Шаблон: "templates/dj_app/product_detail.html"
# Переменная (шаблона/ключ): "product"
class ProductDetailView(DetailView):
    model = Product


# Верификация через почтовый ящик
class EmailVerificationView(TemplateView):
    template_name = 'registration/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))


# Метод Заказы
class OrderCreateView(CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('order_create')

    # для поля с инициатором
    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)


# Класс содержащий ВНУТРЕННЮЮ работу с БД
class DataBase:
    @staticmethod
    # Чтение из таблицы "model" полей которые передаем {} через "kwargs"
    def read(model, mode="all", **kwargs):
        # .count() - метод возвращающий количество
        if mode == "all":  # Получить данные для [всех объектов]
            result = model.objects.all()
            return list(result.values())
        if mode == "filter":  # Получить данные [все которые = фильтр]
            result = model.objects.filter(**kwargs)
            return list(result.values())
        if mode == "exclude":  # Получить данные [все которые = не фильтр]
            result = model.objects.exclude(**kwargs)
            return list(result.values())
        if mode == "get":  # Получить данные для [одного объекта]
            result = model.objects.get(**kwargs)  # id/pk одно и тоже
            print(result, type(result))
            return [result]

    @staticmethod
    # Запись в таблицу "model" полей которые передаем {} через "kwargs"
    def write(model, **kwargs):
        model(**kwargs).save()  # или Person.objects.create(**kwargs)

    @staticmethod
    # Обновление объекта с "elm_id" в таблице "model", а именно перезапись полей на те, которые в {} через "kwargs"
    def update(model, elm_id, **kwargs):
        model.objects.filter(id=elm_id).update(**kwargs)

    @staticmethod
    # Удаление из таблицы "model" записи, удовлетворяющей фильтру переданному в {} через "kwargs"
    def delete(model, **kwargs):
        model.objects.filter(**kwargs).delete()

    @staticmethod
    # Преобразование queryset в list в зависимости от режима "mode"
    def queryset_to_list(qs, mode=""):
        if mode == "elements":  # Финальный список из (элементов)
            result = []
            for elm in qs:
                result.append(elm)
            return result
        if mode == "name":  # Финальный список из (названий)
            result = []
            for elm in qs:
                result.append(elm.name)
            return result

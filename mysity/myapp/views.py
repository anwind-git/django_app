from django.views.generic import ListView, CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView
from django.utils import timezone
from .utils import *
from .forms import *
from .models import *
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('./logs/info.log')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def contacts(request):
    logger.info('Просмотр страницы, информация о сайте'),
    return render(request, 'myapp/contacts.html', {'title': 'Контакты'})


class OpenUser(DataMixin, ListView):
    model = Orders
    template_name = 'myapp/user.html'
    context_object_name = 'orders'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=f'Профиль пользователя {self.request.user.username}')

        week_ago = timezone.now() - timezone.timedelta(days=7)
        month_ago = timezone.now() - timezone.timedelta(days=30)
        year_ago = timezone.now() - timezone.timedelta(days=365)

        user_id = self.request.user.id

        orders_week = Orders.objects.filter(customer_id=user_id, created__gte=week_ago)
        orders_month = Orders.objects.filter(customer_id=user_id, created__gte=month_ago)
        orders_year = Orders.objects.filter(customer_id=user_id, created__gte=year_ago)

        products_week = [str(i) for i in OrderItem.objects.filter(order__in=orders_week).order_by('-order__created')]
        context['products_week'] = set(products_week)

        products_month = [str(i) for i in OrderItem.objects.filter(order__in=orders_month).order_by('-order__created')]
        context['products_month'] = set(products_month)

        products_year = [str(i) for i in OrderItem.objects.filter(order__in=orders_year).order_by('-order__created')]
        context['products_year'] = set(products_year)

        context.update(c_def)

        return context

    def get_queryset(self):
        return Orders.objects.filter(customer_id=self.request.user.id)


class UserEdit(DataMixin, UpdateView):
    form_class = UserEditForm
    template_name = 'myapp/edit.html'
    success_url = reverse_lazy('myapp:profile')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Редактирование пользователя")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class ProductsHome(DataMixin, ListView):
    model = Products
    template_name = 'myapp/index.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Популярные товары магазина')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Products.objects.filter(publication=True)


class ProductsCategory(DataMixin, ListView):
    model = Products
    template_name = 'myapp/index.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=f'Категория - {str(MenuCategories.objects.get(slug=self.kwargs["cat_slug"]))}',
                                      cat_selected=self.kwargs['cat_slug'])
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Products.objects.filter(menu_categories__slug=self.kwargs['cat_slug'], publication=True).exclude(id__in=self.get_cart())


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'myapp/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('myapp:profile')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'myapp/index.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('myapp:profile')


def logout_user(request):
    logout(request)
    return redirect('myapp:login')
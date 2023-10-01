from .models import *
from django.db.models import *


profile_menu = [{'title': 'Профиль', 'url_name': 'user'},
                {'title': 'Заказы', 'url_name': 'user_orders'}
                ]


class DataMixin:
    def get_cart(self):
        product_ids_in_cart = map(str, self.request.session.get('cart', {}).keys())
        return product_ids_in_cart

    def get_user_context(self, **kwargs):
        context = kwargs
        categories = MenuCategories.objects.annotate(Count('products')).order_by('queue')
        context['profile_menu'] = profile_menu
        context['categories'] = categories
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context

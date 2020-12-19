from django.shortcuts import render
from mainapp.models import Product, ProductCategory


def main(request):
    context = {
        'titlepage': 'главная',

    }
    return render(request, 'mainapp/index.html', context = context)


def products(request, pk = None):
    contex = {
        'titlepage': 'каталог товаров',
        'products': Product.objects.all(),
        'catalogs': ProductCategory.objects.all(),
    }

    return render(request, 'mainapp/products.html', context = contex)


def text_context(request):
    context = {
        'title': 'добро пожаловать!',
        'username': 'Andrew',
        'products': [
            {'name': 'Четное худи', 'price': '2 990 руб'},
            {'name': 'Джинсы', 'price': '5 800 руб'}
        ],
        'promotion_products': [
            {'name': 'Туфли', 'price': '10 990 руб'},
        ]
    }
    return render(request, 'mainapp/context.html', context)

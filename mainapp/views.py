from django.shortcuts import render
from mainapp.models import Product, ProductCategory

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def main(request):
    context = {
        'titlepage': 'главная',

    }
    return render(request, 'mainapp/index.html', context = context)


def products(request, category_id = None, page = 1):

    context = {
        'titlepage': 'каталог товаров',
        'catalogs': ProductCategory.objects.all(),
    }
    if category_id:
        products = Product.objects.filter(category_id = category_id).order_by('price')
    else:
        products = Product.objects.all().order_by('price')

    paginator = Paginator(products, 3)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)
    context.update({'products': products_paginator})

    return render(request, 'mainapp/products.html', context = context)


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

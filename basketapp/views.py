from django.shortcuts import HttpResponseRedirect, get_object_or_404
from mainapp.models import Product
from basketapp.models import Basket
from django.contrib import messages


def basket_add(request, id_product=None):
    product = get_object_or_404(Product, id=id_product)
    if product.quantity == 0:
        messages.error(request, 'Такого товара сейчас нет в наличие или он зарезервирован!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        basket = Basket(user=request.user, product=product)
        # basket.quantity += 1
        # product.quantity -= 1
        # basket.save()
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        basket = baskets.first()
    basket.quantity += 1
    product.quantity -= 1
    product.save()
    basket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def basket_remove(request, id=None):
    basket = Basket.objects.get(id=id)
    product = get_object_or_404(Product, id = basket.product.id)
    product.quantity += basket.quantity
    product.save()
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

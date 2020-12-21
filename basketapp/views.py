from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse

from mainapp.models import Product
from basketapp.models import Basket

@login_required
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

@login_required
def basket_remove(request, id=None):
    basket = Basket.objects.get(id=id)
    product = get_object_or_404(Product, id = basket.product.id)
    product.quantity += basket.quantity
    product.save()
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def basket_edit(request, id, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        basket = Basket.objects.get(id=int(id))
        if quantity > 0:
            basket.quantity = quantity
            basket.save()
        else:
            basket.delete()
        baskets = Basket.objects.filter(user=request.user)
        context = {
            'baskets': baskets,
        }
        result = render_to_string('basket.html', context)
        return JsonResponse({'result': result})

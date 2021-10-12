import uuid
from datetime import datetime
from django.template import loader
from ..shared.alert import Alert, AlertType

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from app.backend.domain.service import product_service
from app.models import Product
from app.backend.application.viewmodel.store_viewmodel import ProductViewModel

def productView(request):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect(reverse('login'))

    isSaved = request.session.get('is_saved', False)
    try:
        del request.session['is_saved']
    except KeyError:
        pass

    isDeleted = request.session.get('is_deleted', False)
    try:
        del request.session['is_deleted']
    except KeyError:
        pass

    isErrorOnDeleted = request.session.get('is_error_on_deleted', False)
    try:
        del request.session['is_error_on_deleted']
    except KeyError:
        pass

    template = loader.get_template('product.html')
    return HttpResponse(template.render({
        'alerts': [Alert(AlertType.SUCCESS, "Success: Product saved")] if isSaved else [Alert(AlertType.SUCCESS, "Success: Product deleted")] if isDeleted else [Alert(AlertType.ERROR, "Error: Product not deleted") if isErrorOnDeleted else None],
        'subject': request.user.username,
        'is_logged': True,
        'products': product_service.listProductsOrderedByName() if request.GET.get('orderByName', False) else product_service.listProducts()
    }, request))

def productViewView(request, productId):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect(reverse('login'))

    product = product_service.findProduct(productId)

    return productManageView(request, True, ProductViewModel(product), True, None)

def productCreateView(request):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect(reverse('login'))

    if request.method == 'POST':
        product = Product(name = request.POST['name'], description = request.POST['description'])

        try:
            product_service.saveProduct(product)
            request.session['is_saved'] = True
            return HttpResponseRedirect(reverse('product'))
        except Exception as e:
            return productManageView(request, False, ProductViewModel(product), True, [Alert(AlertType.ERROR, e.message)])

    else:
        return productManageView(request, False, ProductViewModel(), True, None)

def productEditView(request, productId):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect(reverse('login'))

    product = product_service.findProduct(productId)

    if request.method == 'POST':
        product.name = request.POST['name']
        product.description = request.POST['description']

        try:
            product_service.saveProduct(product)
            request.session['is_saved'] = True
            return HttpResponseRedirect(reverse('product'))
        except Exception as e:
            return productManageView(request, False, ProductViewModel(product), True, [Alert(AlertType.ERROR, e.message)])

    else:
        return productManageView(request, False, ProductViewModel(product), True, None)

def productManageView(request, isView, product, isLogged, alerts):
    template = loader.get_template('product_manage.html')
    return HttpResponse(template.render({
        'alerts': alerts,
        'subject': request.user.username,
        'is_logged': isLogged,
        'is_view': isView,
        'product': product
    }, request))

def productRemoveView(request, productId):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect(reverse('login'))

    if request.POST['confirmation_form_response'] == 'N':
        return HttpResponseRedirect(reverse('product'))

    try:
        product = product_service.findProduct(productId)
        product_service.deleteProduct(product)
        request.session['is_deleted'] = True
        return HttpResponseRedirect(reverse('product'))

    except Exception as e:
        request.session['is_error_on_deleted'] = True
        return HttpResponseRedirect(reverse('product'))

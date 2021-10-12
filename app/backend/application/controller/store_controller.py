import uuid
from datetime import datetime
from django.template import loader
from ..shared.alert import Alert, AlertType

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from app.backend.domain.service import store_service
from app.models import Store
from app.backend.application.viewmodel.store_viewmodel import StoreViewModel

def storeView(request):
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

    template = loader.get_template('store.html')
    return HttpResponse(template.render({
        'alerts': [Alert(AlertType.SUCCESS, "Success: Store saved")] if isSaved else [Alert(AlertType.SUCCESS, "Success: Store deleted")] if isDeleted else [Alert(AlertType.ERROR, "Error: Store not deleted") if isErrorOnDeleted else None],
        'subject': request.user.username,
        'is_logged': True,
        'stores': store_service.listStoresOrderedByName() if request.GET.get('orderByName', False) else store_service.listStores()
    }, request))

def storeViewView(request, storeId):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect(reverse('login'))

    store = store_service.findStore(storeId)

    return storeManageView(request, True, StoreViewModel(store), store_service.getAvailableProductsAsKeyValue(storeId), True, None)

def storeCreateView(request):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect(reverse('login'))

    if request.method == 'POST':
        store = Store(name = request.POST['name'], launched_at = datetime.strptime(request.POST['launched_at'], '%d/%m/%Y'))

        productNames = []
        for key in request.POST:
            if key.startswith("product_"):
                productNames.append(key.replace("product_", ""))

        try:
            store_service.saveStore(store)
            store_service.appendProductsToStore(store.id, productNames)
            request.session['is_saved'] = True
            return HttpResponseRedirect(reverse('store'))
        except Exception as e:
            return storeManageView(request, False, StoreViewModel(store), store_service.getAvailableProductsAsKeyValue(), True, [Alert(AlertType.ERROR, e.message)])

    else:
        return storeManageView(request, False, StoreViewModel(), store_service.getAvailableProductsAsKeyValue(), True, None)

def storeEditView(request, storeId):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect(reverse('login'))

    store = store_service.findStore(storeId)

    if request.method == 'POST':
        store.name = request.POST['name']
        store.launched_at = datetime.strptime(request.POST['launched_at'], '%d/%m/%Y')

        productNames = []
        for key in request.POST:
            if key.startswith("product_"):
                productNames.append(key.replace("product_", ""))

        try:
            store_service.saveStore(store)
            store_service.appendProductsToStore(store.id, productNames)
            request.session['is_saved'] = True
            return HttpResponseRedirect(reverse('store'))
        except Exception as e:
            return storeManageView(request, False, StoreViewModel(store), store_service.getAvailableProductsAsKeyValue(storeId), True, [Alert(AlertType.ERROR, e.message)])

    else:
        return storeManageView(request, False, StoreViewModel(store), store_service.getAvailableProductsAsKeyValue(storeId), True, None)

def storeManageView(request, isView, store, productsAsKeyValue, isLogged, alerts):
    template = loader.get_template('store_manage.html')
    return HttpResponse(template.render({
        'alerts': alerts,
        'subject': request.user.username,
        'is_logged': isLogged,
        'is_view': isView,
        'store': store,
        'productsAsKeyValue': productsAsKeyValue
    }, request))

def storeRemoveView(request, storeId):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect(reverse('login'))

    if request.POST['confirmation_form_response'] == 'N':
        return HttpResponseRedirect(reverse('store'))

    try:
        store = store_service.findStore(storeId)
        store_service.deleteStore(store)
        request.session['is_deleted'] = True
        return HttpResponseRedirect(reverse('store'))

    except Exception as e:
        request.session['is_error_on_deleted'] = True
        return HttpResponseRedirect(reverse('store'))

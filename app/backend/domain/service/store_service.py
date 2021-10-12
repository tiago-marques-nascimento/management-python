from app.models import Store, StoreProduct, Product
from app.backend.application.viewmodel.store_viewmodel import StoreViewModel
from app.backend.application.viewmodel.keyvalue_viewmodel import KeyValueViewModel
from ..exception.exception import ValidationError

def listStores():
    return map(lambda store: StoreViewModel(store), Store.objects.all())

def listStoresOrderedByName():
    return map(lambda store: StoreViewModel(store), Store.objects.all().order_by('name'))

def saveStore(store):
    stores = Store.objects.filter(name = store.name)

    isNewStoreButNameAlreadyExistsInDatabase = (store.id is None and stores.count() > 0)
    isExistingStoreButNameAlreadyExistsInDatabase = (store.id is not None and stores.count() > 0 and stores[0].id != store.id)
    if isNewStoreButNameAlreadyExistsInDatabase or isExistingStoreButNameAlreadyExistsInDatabase:
        raise ValidationError('A store with name %s already exists' % store.name)

    store.save()

def findStore(storeId):
    return Store.objects.filter(id = storeId)[0]

def deleteStore(store):
    store.delete()

def getAvailableProductsAsKeyValue(storeId = None):
    storeProducts = [] if storeId == None else StoreProduct.objects.filter(store_id = storeId)
    products = Product.objects.all()
    return map(lambda product: KeyValueViewModel(product.name, hasAnyStoreProduct(product.id, storeProducts)), products)

def hasAnyStoreProduct(productId, storeProducts):
    for storeProduct in storeProducts:
        if storeProduct.product_id == productId:
            return True

    return False

def appendProductsToStore(storeId, productNames):
    storeProducts = StoreProduct.objects.filter(store_id = storeId).delete()
    for productName in productNames:
        storeProduct = StoreProduct(store_id = storeId, product_id = Product.objects.filter(name = productName)[0].id)
        storeProduct.save()

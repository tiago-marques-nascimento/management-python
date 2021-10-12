from app.models import Product
from app.backend.application.viewmodel.store_viewmodel import ProductViewModel
from ..exception.exception import ValidationError

def listProducts():
    return map(lambda product: ProductViewModel(product), Product.objects.all())

def listProductsOrderedByName():
    return map(lambda product: ProductViewModel(product), Product.objects.all().order_by('name'))

def saveProduct(product):
    products = Product.objects.filter(name = product.name)

    isNewProductButNameAlreadyExistsInDatabase = (product.id is None and products.count() > 0)
    isExistingProductButNameAlreadyExistsInDatabase = (product.id is not None and products.count() > 0 and products[0].id != product.id)
    if isNewProductButNameAlreadyExistsInDatabase or isExistingProductButNameAlreadyExistsInDatabase:
        raise ValidationError('A product with name %s already exists' % product.name)

    product.save()

def findProduct(productId):
    return Product.objects.filter(id = productId)[0]

def deleteProduct(product):
    product.delete()

from django.shortcuts import render
from django.template import loader

# Create your views here.
from django.http import HttpResponse
from .backend.application.controller import login_controller, home_controller, store_controller, product_controller

def loginView(request):
    return login_controller.loginView(request)

def logoutView(request):
    return login_controller.logoutView(request)

def homeView(request):
    return home_controller.homeView(request)

#Store
def storeView(request):
    return store_controller.storeView(request)

def storeViewView(request, store_id):
    return store_controller.storeViewView(request, store_id)

def storeCreateView(request):
    return store_controller.storeCreateView(request)

def storeEditView(request, store_id):
    return store_controller.storeEditView(request, store_id)

def storeRemoveView(request, store_id):
    return store_controller.storeRemoveView(request, store_id)

#Product
def productView(request):
    return product_controller.productView(request)

def productViewView(request, product_id):
    return product_controller.productViewView(request, product_id)

def productCreateView(request):
    return product_controller.productCreateView(request)

def productEditView(request, product_id):
    return product_controller.productEditView(request, product_id)

def productRemoveView(request, product_id):
    return product_controller.productRemoveView(request, product_id)

from django.urls import path

from . import views

urlpatterns = [
    path('login', views.loginView, name = "login"),
    path('logout', views.logoutView, name = "logout"),
    path('home', views.homeView, name = "home"),
    path('store', views.storeView, name = "store"),
    path('store/<uuid:store_id>/view', views.storeViewView, name = "store_view"),
    path('store/create', views.storeCreateView, name = "store_create"),
    path('store/<uuid:store_id>/edit', views.storeEditView, name = "store_edit"),
    path('store/<uuid:store_id>/remove', views.storeRemoveView, name = "store_remove"),
    path('product', views.productView, name = "product"),
    path('product/<uuid:product_id>/view', views.productViewView, name = "product_view"),
    path('product/create', views.productCreateView, name = "product_create"),
    path('product/<uuid:product_id>/edit', views.productEditView, name = "product_edit"),
    path('product/<uuid:product_id>/remove', views.productRemoveView, name = "product_remove")
]

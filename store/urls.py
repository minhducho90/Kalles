from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
    path('', views.index, name='index'),
    path('subcategory/<slug:slug>/', views.productlist, name='product_list'),
    path('product/<int:pk>', views.productdetail, name='product_detail'),
    path('search/', views.search, name='search'),
    path('contact/', views.contact, name='contact'),
    path('api/all-products/', views.products_service),
    path('api/product-detail/<int:pk>/', views.product_service_detail),
]
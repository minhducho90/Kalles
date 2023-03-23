from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from rest_framework import viewsets
from store.models import Category, SubCategory, Product, Contact
from .forms import FormContact
from .serializers import ProductSerializer
from cart.cart import Cart
import random


# Cach 2
# from . models import Category, SubCategory, Product


def index(request):
    cart = Cart(request)
    sub_cats = SubCategory.objects.all()
    all_product = Product.objects.all()
    n = 12
    random_product = random.sample(list(all_product), n)
    # tbgd_subcategory = SubCategory.objects.filter(category=1)
    # filter theo slug
    phong_khach = SubCategory.objects.filter(category__slug='phong-khach').values_list('slug')
    phong_an = SubCategory.objects.filter(category__slug='phong-an').values_list('slug')
    ban_lam_viec = SubCategory.objects.filter(category__slug='ban-lam-viec').values_list('slug')
    ngoai_that = SubCategory.objects.filter(category__slug='ngoai-that').values_list('slug')

    pk_list_sub = []
    pa_list_sub = []
    blv_list_sub = []
    nt_list_sub = []

    for sub in phong_khach:
        pk_list_sub.append(sub[0])

    for sub in phong_an:
        pa_list_sub.append(sub[0])

    for sub in ban_lam_viec:
        blv_list_sub.append(sub[0])

    for sub in ngoai_that:
        nt_list_sub.append(sub[0])

    pk_products = Product.objects.filter(subcategory__slug__in=pk_list_sub)[:12]
    pa_products = Product.objects.filter(subcategory__slug__in=pa_list_sub)[:12]
    blv_products = Product.objects.filter(subcategory__slug__in=blv_list_sub)[:12]
    nt_products = Product.objects.filter(subcategory__slug__in=nt_list_sub)[:12]

    return render(request, 'store/index.html', {
        'pk_products': pk_products,
        'pa_products': pa_products,
        'blv_products': blv_products,
        'nt_products': nt_products,
        'cart': cart,
        'sub_cats': sub_cats,
        'best_sale': random_product,
    })


def productlist(request, slug):
    cart = Cart(request)
    sub_cats = SubCategory.objects.all()

    if slug == 'tat-ca-san-pham':
        products = Product.objects.all()
        sub_name = 'Tất cả sản phẩm (' + str(len(products)) + ')'
    else:
        products = Product.objects.filter(subcategory__slug=slug)
        select_name = SubCategory.objects.get(slug=slug)
        sub_name = select_name.name + ' (' + str(len(products)) + ')'
    # lọc giá
    from_price = 0
    to_price = 0

    if request.GET.get('from_price'):
        from_price = int(request.GET.get('from_price'))
        to_price = int(request.GET.get('to_price'))
        products = [product for product in products if from_price <= product.price <= to_price] # list comprehension
        sub_name = f'Số sản phẩm có giá từ "{from_price} VND" đến "{to_price} VND" là: ' + ' (' + str(len(products)) + ')'

    # Phân trang
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 24)
    product_page = paginator.page(page)

    return render(request, 'store/shop-right-sidebar.html', {
        'slug': slug,
        'sub_name': sub_name,
        'sub_cats': sub_cats,
        'products': product_page,
        'from_price': from_price,
        'to_price': to_price,
        'cart': cart
    })


def productdetail(request, pk):
    cart = Cart(request)
    all_product = Product.objects.all()
    product = Product.objects.get(pk=pk)
    sub_category_id = Product.objects.filter(pk=pk).values_list('subcategory')
    product_related = Product.objects.filter(subcategory__in=sub_category_id).exclude(pk=pk)[:9]
    sub_cats = SubCategory.objects.all()
    n = 5
    random_product = random.sample(list(all_product), n)

    return render(request, 'store/product-bottom-thumbnail.html', {
        'product': product,
        'product_related': product_related,
        'sub_cats': sub_cats,
        'random_product': random_product,
        'cart': cart
    })


def search(request):
    cart = Cart(request)
    if request.GET.get('product_name') and request.GET.get('product_name') != '':
        sub_cats = SubCategory.objects.all()
        product_name = request.GET.get('product_name').strip()
        search_products = Product.objects.filter(name__contains=product_name)
        search_name = f'Số sản phẩm có từ khóa "{product_name}": ' + '(' + str(len(search_products)) + ')'
    else:
        sub_cats = SubCategory.objects.all()
        search_products = Product.objects.all()
        search_name = f'Số sản phẩm có từ khóa "": ' + '(' + str(len(search_products)) + ')'
    page = request.GET.get('page', 1)
    paginator = Paginator(search_products, 24)
    product_page = paginator.page(page)

    return render(request, 'store/search.html', {
        'sub_cats': sub_cats,
        'products': product_page,
        'search_name': search_name,
        'cart': cart
    })


def contact(request):
    cart = Cart(request)
    form = FormContact()
    result = ''

    if request.POST.get('btnSend'):
        form = FormContact(request.POST, Contact)
        if form.is_valid():
            post = form.save(commit=False)
            post.first_name = form.cleaned_data['first_name']
            post.last_name = form.cleaned_data['last_name']
            post.phone_number = form.cleaned_data['phone_number']
            post.email = form.cleaned_data['email']
            post.message = form.cleaned_data['message']
            post.save()

            result = '''
                <div class="alert alert-success" role="alert">
                    Submit Successfully!!!
                </div>
            '''

    return render(request, 'store/contact-us.html', {
        'form': form,
        'result': result,
        'cart': cart
    })


def products_service(request):
    product = Product.objects.all()
    result_list = list(product.values('name', 'price', 'content', 'image'))

    return JsonResponse(result_list, safe=False)


def product_service_detail(request,pk):
    product = Product.objects.filter(pk=pk)
    result_list = list(product.values())[0]

    return JsonResponse(result_list, safe=False)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
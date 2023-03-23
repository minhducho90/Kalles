from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import PBKDF2SHA1PasswordHasher
from django.contrib.auth.models import User
from .models import Customer
from .forms import FormUser, FormCustomer
from cart.models import Order, OrderItem
from cart.cart import Cart
from store.models import Product


def register(request):
    form_user = FormUser()
    form_customer = FormCustomer()
    result_register = ''

    if request.POST.get('btnRegister'):
        form_user = FormUser(request.POST)
        form_customer = FormCustomer(request.POST)
        if form_user.is_valid() and form_customer.is_valid():
            if form_user.cleaned_data['password'] == form_user.cleaned_data['confirm_password']:
                # user
                user = form_user.save()
                user.set_password(user.password)
                user.save()
                # customer
                customer = form_customer.save()
                customer.user = user
                customer.phone_number = form_customer.cleaned_data['phone_number']
                customer.address = form_customer.cleaned_data['address']
                customer.save()
                result_register = '''
                        <div class="alert alert-success" role="alert">
                            Submit Successfully!!! Đã đăng ký thành công
                        </div>
                    '''
        else:
            result_register = '''
                        <div class="alert alert-success" role="alert">
                            Submit False!!! Đăng ký thất bại
                        </div>
                    '''
    return render(request, 'users/register.html', {
        'form_user': form_user,
        'form_customer': form_customer,
        'result_register': result_register
    })


def signin(request):
    form_signin = FormUser()
    result_login = ''

    if request.POST.get('btnSignin'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('store:index')
        else:
            result_login = '''
                                <div class="alert alert-success" role="alert">
                                    Đăng nhập thất bại
                                </div>
                            '''

    return render(request, 'users/signin.html', {
        'form_signin': form_signin,
        'result_login': result_login
    })


def forgot(request):
    return render(request, 'users/forgot.html')


def user_logout(request):
    logout(request)

    return redirect('users:login')


def myaccount(request):
    if not request.user.username:
        return redirect('user:login')
    cart = Cart(request)

    if request.POST.get('btnUpdateUser'):
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')

        s_user = request.user
        customer = Customer.objects.get(user__id=s_user.id)
        customer.user.last_name = last_name
        customer.user.first_name = first_name
        customer.user.email = email
        customer.phone_number = phone_number
        customer.address = address
        customer.save()

        s_user.last_name = last_name
        s_user.first_name = first_name
        s_user.email = email

        messages.success(request, "Đã cập nhật thông tin thành công")

    orders = Order.objects.filter(username=request.user.username)
    customer = Customer.objects.get(user__id=request.user.id)
    dict_orders = {}
    for order in orders:
        items = list(OrderItem.objects.filter(order=order.id).values())
        for item in items:
            product = Product.objects.get(id=item['product_id'])
            item['product_name'] = product.name
            item['product_image'] = product.image
            item['total_price'] = order.total
        else:
            dict_order_items = {
                order.id: items
            }
            dict_orders.update(dict_order_items)

    return render(request, 'users/my-account.html', {
        'cart': cart,
        'orders': orders,
        'dict_orders': dict_orders,
        'customer': customer
    })

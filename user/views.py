from django.shortcuts import render, redirect, reverse
from django.http.response import JsonResponse
import string
import random
from django.core.mail import send_mail
from .models import CaptchaModel, UserDetail
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm, ModifyForm, ResetForm, ModifyPasswordForm
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.models import User
from myblog.models import Blog
from cuisine.models import Cuisine
from home.models import FavoriteWindow

User = get_user_model()


@require_http_methods(['GET'])
def mylogin(request):
    if request.method == 'GET':
        return render(request, 'user/login.html')


def check_login(request, email, password, remember):
    user = User.objects.filter(email=email).first()
    if user and user.check_password(password):
        login(request, user)
        if remember == 0:
            request.session.set_expiry(0)
        return JsonResponse({"code": 200})
    elif not user:
        return JsonResponse({"code": 400, "message": '不存在此邮箱！'})
    elif not user.check_password(password):
        return JsonResponse({"code": 400, "message": '密码错误！'})


def mylogout(request):
    logout(request)
    return redirect(reverse('user:login'))


@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == 'GET':
        return render(request, 'user/register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(email=email, username=username, password=password)
            UserDetail.objects.create(user=user)
            return redirect(reverse('user:login'))
        else:
            print(form.errors)
            return redirect(reverse('user:register'))


def send_email_captcha(request):
    email = request.GET.get('email')
    if not email:
        return JsonResponse({"code": 400, "message": '邮箱格式错误！'})
    captcha = "".join(random.sample(string.digits, 4))
    users = User.objects.filter(email=email)
    if not users.exists():
        CaptchaModel.objects.update_or_create(email=email, defaults={'captcha': captcha})
        send_mail("注册验证", message=f"您的注册验证码是：{captcha}", recipient_list=[email], from_email=None)
        return JsonResponse({"code": 200, "message": '验证码发送成功！'})
    else:
        return JsonResponse({"code": 400, "message": '此邮箱已被注册！'})


@require_http_methods(['GET', 'POST'])   
def forget(request):
    if request.method == 'GET':
        return render(request, 'user/forget.html')
    else:
        form = ResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            captcha = form.cleaned_data.get('captcha')
            print(password, captcha)
            c = CaptchaModel.objects.filter(captcha=captcha, email=email).first()
            if not c:
                return redirect(reverse('user:forget'))
            user = User.objects.filter(email=email).first()
            user.set_password(password)
            user.save()
            return redirect(reverse('user:login'))
        else:
            print(form.errors)
            return redirect(reverse('user:forget'))


def send_email_reset(request):
    email = request.GET.get('email')
    if not email:
        return JsonResponse({"code": 400, "message": '邮箱格式错误！'})
    captcha = "".join(random.sample(string.digits, 4))
    users = User.objects.filter(email=email)
    if users.exists():
        CaptchaModel.objects.update_or_create(email=email, defaults={'captcha': captcha})
        send_mail("忘记密码", message=f"您的重置密码验证码是：{captcha}", recipient_list=[email], from_email=None)
        return JsonResponse({"code": 200, "message": '验证码发送成功！'})
    else:
        return JsonResponse({"code": 400, "message": '此邮箱尚未注册！'})


def center(request):
    context = {
        'user': request.user,
    }
    return render(request, 'user/center.html', context=context)


def modify(request):
    if request.method == 'GET':
        context = {
            'user': request.user,
        }
        return render(request, 'user/modify.html', context=context)
    else:
        form = ModifyForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            user.username = form.cleaned_data.get('username')
            userdetail = UserDetail.objects.get(user=user)
            userdetail.age = form.cleaned_data.get('age')
            userdetail.gender = form.cleaned_data.get('gender')
            userdetail.height = form.cleaned_data.get('height')
            userdetail.weight = form.cleaned_data.get('weight')
            user.save()
            userdetail.save()
            return redirect(reverse('user:center'))
        else:
            print(form.errors)
            return redirect(reverse('user:center'))


def modify_password(request):
    if request.method == 'GET':
        context = {
            'user': request.user,
        }
        return render(request, 'user/modify_password.html', context=context)
    else:
        form = ModifyPasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            return redirect(reverse('user:login'))
        else:
            print(form.errors)
            return redirect(reverse('user:center'))


def upload_avatar(request):
    return render(request, 'user/upload_avatar.html')


def handle_avatar(request):
    file = request.FILES.get('avatar')
    user_detail = UserDetail.objects.get(user=request.user)
    user_detail.avatar = file
    user_detail.save()
    return redirect(reverse('user:center'))


def history_pub(request):
    context = {
        'pub_blogs': Blog.objects.filter(author=request.user)
    }
    return render(request, 'user/history_pub.html', context=context)


def history_like(request):
    context = {
        'liked_blogs': Blog.objects.filter(likes__user=request.user)
    }
    return render(request, 'user/history_like.html', context=context)


def history_favorite(request):
    context = {
        'favorite_cuisines': Cuisine.objects.filter(favorites__user=request.user)
    }
    return render(request, 'user/history_favorite.html', context=context)


def history_eaten(request):
    context = {
        'eaten_cuisines': Cuisine.objects.filter(eatens__user=request.user)
    }
    return render(request, 'user/history_eaten.html', context=context)


def history_window(request):
    context = {
        'favorite_windows': FavoriteWindow.objects.filter(user=request.user)
    }
    return render(request, 'user/history_window.html', context=context)
        
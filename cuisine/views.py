from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST, require_GET

import random
import user.models
from .models import Cuisine, CuisineComment, FavoriteCuisine, EatenCuisine, StarCuisine
from user.models import UserDetail
from django.db.models import Q


# Create your views here.
def cuisine_detail(request, cuisine_id):
    cuisine = Cuisine.objects.get(pk=cuisine_id)
    favorite_cuisine = cuisine.favorites.filter(user=request.user).exists()
    eaten_cuisine = cuisine.eatens.filter(user=request.user).exists()
    if 'starNum' in request.GET:
        star = request.GET['starNum']
        starCuisine = StarCuisine.objects.filter(user=request.user, cuisine=cuisine).first()
        if not starCuisine:
            StarCuisine.objects.create(star=star, user=request.user, cuisine=cuisine)
        else:
            starCuisine.star = star
            starCuisine.save()
    mark_stars = StarCuisine.objects.filter(cuisine=cuisine).all()
    star_sum = 0
    for mark_star in mark_stars:
        star_sum += mark_star.star
    if mark_stars.count() == 0:
        cuisine.star_ave = -1
    else:
        cuisine.star_ave = star_sum / mark_stars.count()
    cuisine.save()
    
    context = {
        'cuisine': cuisine,
        'username': request.user.username,
        'favorite_cuisine': favorite_cuisine,
        'eaten_cuisine': eaten_cuisine,
    }
    return render(request, 'cuisine/cuisine_detail.html', context=context)


@require_POST
@login_required()
def pub_comment(request):
    cuisine_id = request.POST.get('cuisine_id')
    content = request.POST.get('content')
    CuisineComment.objects.create(content=content, cuisine_id=cuisine_id, author=request.user)
    return redirect(f'/cuisine/{cuisine_id}')


@require_GET
def search(request):
    # /search?q=xxx
    q = request.GET.get('q')
    cuisines = Cuisine.objects.filter(Q(name__icontains=q)|Q(tag1__exact=q)|Q(tag2__exact=q)|Q(tag3__exact=q)).all()
    context = {
        "cuisines": cuisines,
        'user': request.user,
    }
    return render(request, 'cuisine/cuisine_search.html', context=context)


@login_required
def favor_cuisine(request, cuisine_id):
    cuisine = get_object_or_404(Cuisine, id=cuisine_id)
    favor, created = FavoriteCuisine.objects.get_or_create(user=request.user, cuisine=cuisine)
    if not created:
        favor.delete()
    return redirect(reverse("cuisine:cuisine_detail", kwargs={'cuisine_id': cuisine_id}))


@login_required
def eaten_cuisine(request, cuisine_id):
    cuisine = get_object_or_404(Cuisine, id=cuisine_id)
    eaten, created = EatenCuisine.objects.get_or_create(user=request.user, cuisine=cuisine)
    if not created:
        eaten.delete()
    return redirect(reverse("cuisine:cuisine_detail", kwargs={'cuisine_id': cuisine_id}))


@login_required
def recommend(request):
    user_detail = UserDetail.objects.get(user=request.user)
    weight = user_detail.weight
    height = user_detail.height
    gender = user_detail.gender
    age = user_detail.age
    if height != 0:
        height = float(height) / 100
        bmi = round(weight / (height * height), 2)
    else:
        bmi = -1
    if bmi > 25.0:
        hun_max = 4
        su_max = 2
    elif bmi <= 18.0:
        hun_max = 4
        su_max = 2
    else:
        hun_max = 3
        su_max = 3
    if gender == '男' or gender == '男性':
        hun_max += 1
        su_max -= 1
    else:
        hun_max -= 1
        su_max += 1
    if age >= 60:
        hun_max -= 1
        su_max += 1
    
    cuisines = list(Cuisine.objects.all())
    random.shuffle(cuisines)
    random_skip = random.randint(0,200)
    result = []
    i = 0
    hun_count = 0
    su_count = 0
    sum_count = 0
    for cuisine in cuisines:
        if i > random_skip:
            if (cuisine.tag1 == '素' or cuisine.tag2 == '素' or cuisine.tag3 == '素') \
                    and su_count < su_max and (not cuisine in result):
                result.append(cuisine)
                su_count += 1
                sum_count += 1
            elif (cuisine.tag1 == '荤' or cuisine.tag2 == '荤' or cuisine.tag3 == '荤') \
                    and hun_count < hun_max and (not cuisine in result):
                result.append(cuisine)
                hun_count += 1
                sum_count += 1
        i += 1
        if sum_count == 6:
            break
    context = {
        "bmi": bmi,
        "recommend_cuisines": result,
        "eaten_cuisines": Cuisine.objects.filter(eatens__user=request.user)[:6],
        "favor_cuisines": Cuisine.objects.filter(favorites__user=request.user)[:6],
        "highest_star_cuisines": Cuisine.objects.exclude(star_ave=-1).order_by('-star_ave')[:9],
    }
    return render(request, 'cuisine/cuisine_rec.html', context=context)

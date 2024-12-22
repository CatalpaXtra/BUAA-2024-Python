from django.shortcuts import render, redirect, reverse
from cuisine.models import Cuisine
from user.models import UserDetail
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.db.models import Q
from .models import FavoriteWindow

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        user = request.user
        context = {
            'user': user,
            'userdetail': UserDetail.objects.filter(user=user).first(),
            'cuisines': Cuisine.objects.all(),
        }
    else:
        user = None
        context = {
            'user': user,
            'userdetail': None,
            'cuisines': Cuisine.objects.all(),
        }
    return render(request, 'home.html', context=context)


def map(request):
    return render(request, 'map.html')


def cafeteria_transfer(cafeteria):
    if cafeteria == 'heyi':
        return '合一'
    elif cafeteria == 'xueer':
        return '学二'
    elif cafeteria == 'xinbei':
        return '新北'


def floor_transfer(floor):
    print(str(floor))
    if floor == 1:
        return '一楼'
    elif floor == 2:
        return '二楼'
    elif floor == 3:
        return '三楼'
    elif floor == 4:
        return '四楼'
    elif floor == 0:
        return 'B1'


def window_transfer(window):
    # meal
    #合一二楼
    if window == 'jingpin':
        return '精品菜'
    elif window == 'chuancai':
        return '川菜窗口'
    elif window == 'luwei':
        return '卤味'
    elif window == 'jiachang1':
        return '家常窗口(左）'
    elif window == 'jiachang2':
        return '家常窗口(右)'
    elif window == 'kaofan':
        return '烤饭窗口'
    elif window == 'mianshi':
        return '面食窗口'
    elif window == 'shuijiao':
        return '手工水饺'
    elif window == 'tieban':
        return '铁板炒饭炒面'
    #合一三楼
    elif window == 'siji':
        return '四季窗口'
    elif window == 'kaofan2':
        return '烤饭窗口'
    elif window == 'fengkuang':
        return '疯狂抄手'
    elif window == 'gaijiao':
        return '盖浇饭窗口'
    elif window == 'chongqing':
        return '重庆小面'
    elif window == 'guotie':
        return '锅贴窗口'
    #学二
    elif window == 'taocan':
        return '套餐窗口'
    elif window == 'qingzhen':
        return '清真窗口'
    elif window == 'jingdian':
        return '经典窗口'
    elif window == 'zixuan':
        return '自选窗口'
    #新北负一层
    elif window == 'yuangu':
        return '原蛊蒸饭'
    elif window == 'lushi':
        return '炉石披萨'
    elif window == 'zhaji':
        return '炸鸡汉堡'
    elif window == 'zhuduji':
        return '猪肚鸡'
    elif window == 'wanghong':
        return '王宏龙馋嘴鱼'
    elif window == 'shiguo':
        return '石锅饭'
    elif window == 'mida':
        return '米大碗'
    elif window == 'tiebanchufang':
        return '铁板厨房'
    elif window == 'mianfengwei':
        return '面丰味'
    #新北一楼
    elif window == 'zhushi':
        return '主食窗口'
    elif window == 'lurou':
        return '卤肉饭'
    elif window == 'jiben':
        return '基本伙'
    elif window == 'yufen':
        return '渔粉'
    elif window == 'zibu':
        return '滋补汤品'
    elif window == 'reban':
        return '热拌酱菜'
    elif window == 'jingpin':
        return '精品菜'
    elif window == 'hangwei':
        return '航味菜'
    elif window == 'qingshi':
        return '轻食套餐'
    elif window == 'miantiao':
        return '面条'
    #xinbei 2
    elif window == 'yipin':
        return '一品粥饼'
    elif window == 'wugu':
        return '五谷鱼粉'
    elif window == 'guangshi':
        return '广式腊肠'
    elif window == 'shougong2':
        return '手工水饺'
    elif window == 'guilin':
        return '桂林米粉'
    elif window == 'hunan':
        return '湖南小碗菜'
    elif window == 'jianbing':
        return '煎饼烤冷面'
    elif window == 'gaifan':
        return '盖饭'
    elif window == 'shiguo':
        return '石锅铁板'
    elif window == 'chongqing2':
        return '重庆小面'
    elif window == 'minnan':
        return '闽南浇汁拌饭'
    elif window == 'hundun':
        return '馄饨'
    elif window == 'yuzi':
        return '鱼籽饭'
    elif window == 'huangmen':
        return '黄焖鸡'
    #新北三楼
    elif window == 'nanshi':
        return '南时雨'
    elif window == 'jingcai':
        return '璟采'
    elif window == 'huajian':
        return '花间'
    # drink
    elif window == 'xxyinbabei':
        return '小小饮吧（北侧）'
    elif window == 'xxyinbanan':
        return '小小饮吧（南侧）'
    elif window == 'meng':
        return '檬大咖'
    elif window == 'shuiba':
        return '水吧'
    elif window == 'chama':
        return '茶·麻'

    

def meal_window_detail(request, cafeteria, floor, window):
    path = 'meal/' + cafeteria + '/' + str(floor) + '/' + window
    transfered_cafeteria = cafeteria_transfer(cafeteria)
    transfered_floor = floor_transfer(floor)
    transfered_window = window_transfer(window)
    cuisines = Cuisine.objects.filter(cafeteria=transfered_cafeteria, floor=transfered_floor, window=transfered_window)
    context = {
        'name': transfered_window,
        'window': window,
        'favorite_window': FavoriteWindow.objects.filter(user=request.user, name=transfered_window, path=path).exists(),
        'path': path,
        "cuisines": cuisines,
    }
    return render(request, 'window_detail.html', context=context)


def drink_window_detail(request, cafeteria, floor, window):
    path = 'drink/' + cafeteria + '/' + str(floor) + '/' + window
    transfered_cafeteria = cafeteria_transfer(cafeteria)
    transfered_floor = floor_transfer(floor)
    transfered_window = window_transfer(window)
    cuisines = Cuisine.objects.filter(cafeteria=transfered_cafeteria, floor=transfered_floor, window=transfered_window)
    context = {
        'name': transfered_window,
        'window': window,
        'favorite_window': FavoriteWindow.objects.filter(user=request.user, name=transfered_window, path=path).exists(),
        'path': path,
        "cuisines": cuisines,
    }
    return render(request, 'window_detail.html', context=context)


def breakfast_window_detail(request):
    cuisines = Cuisine.objects.filter(type='breakfast')
    context = {
        'name': '早餐',
        "cuisines": cuisines,
    }
    return render(request, 'window_detail.html', context=context)


def selfselect_window_detail(request, window):
    path = 'selfselect/' + window
    transfered_window = window_transfer(window)
    cuisines = Cuisine.objects.filter(type='selfselect', window=transfered_window)
    context = {
        'name': transfered_window,
        'window': window,
        'favorite_window': FavoriteWindow.objects.filter(user=request.user, name=transfered_window, path=path).exists(),
        'path': path,
        "cuisines": cuisines,
    }
    return render(request, 'window_detail.html', context=context)


def favor_window(request, window, path):
    transfered_window = window_transfer(window)
    favor, created = FavoriteWindow.objects.get_or_create(user=request.user, name=transfered_window, path=path)
    if not created:
        favor.delete()
    redirect_to = request.META.get('HTTP_REFERER', '/')
    
    return redirect(redirect_to)

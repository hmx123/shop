import hashlib
import uuid

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
#fang wen zhu ye
from django.urls import reverse

from App.models import AppHome, HomeNav, HomeBuy, HomeShop, HomeShow, MainMarket, MainGoods, MainUser, MainCart, \
    MainOrder, MainOrderDetail


def home(request):
    top_wheel = AppHome.objects.all()
    navs = HomeNav.objects.all()
    mustbuy = HomeBuy.objects.all()

    shops = HomeShop.objects.all()
    shops_0 = shops[0: 1]
    shops_1_3 = shops[1: 3]
    shops_3_7 = shops[3: 7]
    shops_7_11 = shops[7: 11]

    #fen lei
    shows = HomeShow.objects.all()
    date = {
        'title': 'shouye',
        'top_wheel': top_wheel,
        'navs': navs,
        'buys': mustbuy,
        # 'shops': shops,
        'shops_0': shops_0,
        'shops_1-3': shops_1_3,
        'shops_3_7': shops_3_7,
        'shops_7_11': shops_7_11,
        'shows': shows,

    }
    return render(request, 'home/home.html', context=date)

def market(request):
    # 3zhuan fa
    return HttpResponseRedirect(reverse('app:marketparam', args=('104747', '0', '0', '综合排序', '全部类型' )))
def marketparam(request, typeid, cid, sortid, leiname, sortname ):
    foottypes = MainMarket.objects.all()
    #nei rong
    if cid == '0':
        goods = MainGoods.objects.filter(categoryid=typeid)
    else:
        goods = MainGoods.objects.filter(categoryid=typeid).filter(childcid=cid)

    if sortid == '0':
        pass
    elif sortid == '1':
        goods = goods.order_by('productnum')
    elif sortid == '2':
        goods = goods.order_by('price')
    elif sortid == '3':
        goods = goods.order_by('-price')


    #houqu quanbu leixing
    types1 = MainMarket.objects.filter(typeid=typeid)
    all_type_list = []
    if types1.exists():
        ty = types1.first()
        # ty = MainMarket()
        chilname = ty.childtypenames
        one = chilname.split('#')
        for two in one:
            three = two.split(':')
            all_type_list.append(three)

    # huo qu ren gou wu che shang pin de shu liang
    # panduan ren shi fou deng lu
    utoken = request.COOKIES.get("tokenid")
    user = MainUser.objects.filter(utoken=utoken)
    goodsq = request.POST.get('gid')
    if user.exists():
        u = user.first()
        carts = MainCart.objects.filter(c_user=u)
        for p in goods:
            for c in carts:
                if c.c_goods.productid == p.productid:
                    p.num = c.c_num
                    continue
    date = {
        'title': 'shansong',
        'foottypes': foottypes,
        'goods': goods,
        'typeid': typeid,
        'all_type_list': all_type_list,
        'cid': cid,
        'sortname': sortname,
        'leiname': leiname
    }
    return render(request, 'market/market.html', context=date)
#gou wu che
def cart(request):
    utoken = request.COOKIES.get("tokenid")
    if not utoken:
        return render(request, 'user/user_login.html')
    users = MainUser.objects.filter(utoken=utoken)
    data={}
    if users.exists():
        u = users.first()
        carts = MainCart.objects.filter(c_user=u)
        data = {
            'title': 'gouwu',
            'name': u.name,
            'phone': u.phone,
            'cart': carts,
            'is_select': '0',
            'allselect': '0',
        }
        if carts.exists():
            # for car in carts:
            #     carf = car.is_select
            #     if not carf:
            #         data['allselect'] = '1'
            c = carts.first()
            data['is_select'] = c.is_select
            cartsum = 0
            for cart in carts:
                c = cart.c_num * cart.c_goods.marketprice
                cartsum += c
            cartsum = round(cartsum, 2)
            data['cartsum'] = cartsum

        return render(request, 'cart/cart.html',context=data)
    return render(request, 'user/user_login.html')
def mine(request):
    date = {
        'title': 'wode'

    }
    # huoqu zhan shi de xin xi
    utoken = request.COOKIES.get("tokenid")
    if utoken:
        # cong shu ju kuzhong huoqu shuju
        user = MainUser.objects.filter(utoken=utoken)
        if user.exists():
            u = user.first()
            # u = MainUser()
            uicon = u.icon
            u_name = u.name
            date['uname'] = u_name
            date['uicon'] = "/static/uploads/" + uicon.url
            date['is_login'] = True

    return render(request, 'mine/mine.html', context=date)

def user_register(request):
    method = request.method
    if method == 'GET':
        return render(request, 'user/user_register.html')
    elif method == 'POST':
        uname = request.POST.get('username')
        uphone = request.POST.get('userphone')
        uemail = request.POST.get('useremail')
        upwd = request.POST.get('userpwd')
        ugender = request.POST.get('gender')
        uicon = request.FILES.get('usericon')

        user = MainUser()
        user.name = uname
        user.phone = uphone
        user.email = uemail
        user.pwd = pwd_sha(upwd)
        user.gender = ugender
        user.icon = uicon
        user.save()
        print('goudan')
        return render(request, 'mine/mine.html')


    else:
        raise Exception('qing qiu bu cun zai ')

def pwd_sha(pwd):
    sha = hashlib.sha512()
    sha.update(pwd.encode('utf-8'))
    return sha.hexdigest()

#login
def user_login(request):
    method = request.method
    #jin dao deng lu jie mian
    if method == 'GET':
        return render(request, 'user/user_login.html')
    elif method == 'POST':
        # huoqu ye mian shu ju
        uname = request.POST.get('username')
        upwd = request.POST.get('userpwd')

        user = MainUser.objects.filter(name=uname)
        if user.exists():
            u = user.first()
            if u.pwd == pwd_sha(upwd):
                # jiang ge ren xin xi cun fang dao session
                # request.session['username'] = uname
                token = creat_token()
                u.utoken = token
                u.save()
                resp = HttpResponseRedirect(reverse('app:dologin'))
                resp.set_cookie('tokenid', token)
                return resp
        return redirect(reverse('app:register'))

    else:
        raise Exception('qing qiu bu cun zai ')

#验证登录
def dologin(request):
    utoken = request.COOKIES.get("tokenid")
    if utoken:
        u = MainUser.objects.filter(utoken=utoken)
        if u.exists():
            user = u.first()
            data = {
                'uname': user.name,
                'uicon': user.icon,
                'is_login': True,
            }
            return render(request, 'mine/mine.html', context=data)
    return HttpResponseRedirect(reverse('app:login'))
#生成token
def creat_token():
    token = str(uuid.uuid4())
    token = token.replace('-','')
    return token

# shi yong ajax jian ce yong hu ming shi fou cun fu
def chk_username(request):
    uname = request.GET.get('name')
    data = {
        'code': '200',
        'msg': 'ok'
    }
    users = MainUser.objects.filter(name=uname)
    if users.exists():
        data['desc'] = '已经存在，不可用'
        data['msg'] = 'fail'
        data['code'] = '700'
        return JsonResponse(data)
    else:
        data['desc'] = '该用户名 可用'
        return JsonResponse(data)
#退出
def user_loginout(request):
    utoken = request.COOKIES.get("tokenid")
    user = MainUser.objects.filter(utoken=utoken)
    u = user.first()
    u.utoken = ''
    u.save()
    request.session.flush()
    return render(request, 'mine/mine.html')

#从超市添加
def add_card_num(request):
    #huoqu shu ju
    #session
    utoken = request.COOKIES.get("tokenid")
    user1 = MainUser.objects.filter(utoken=utoken)
    data = {
        'msg':'ok',
        'code':'200',
        'desc': 'sucess'
    }
    if not utoken or not user1.exists():
        data['code'] = '700'
        return JsonResponse(data)
    #ajax
    goodid = request.GET.get('gid')
    users = MainUser.objects.filter(utoken=utoken)
    goods = MainGoods.objects.filter(productid=goodid)
    u = users.first()
    g = goods.first()
    carts = MainCart.objects.filter(c_user=u).filter(c_goods=g)
    if carts.exists():
        c = carts.first()
        c.c_num = c.c_num + 1
        c.save()
        data['cnum'] = c.c_num
    else:
        newCart = MainCart()
        newCart.c_user = u
        newCart.c_goods = g
        newCart.c_num = 1
        newCart.save()
        data['cnum'] = newCart.c_num
    return JsonResponse(data)

#从超市减少
def sub_card_num(request):
    utoken = request.COOKIES.get("tokenid")
    data = {
        'msg': 'ok',
        'code': '200',
        'desc': 'sucess'
    }
    if not utoken:
        data['msg'] = 'fail'
        data['code'] = '700'
        data['desc'] = 'no login'
        return JsonResponse(data)
    goodid = request.GET.get('sid')
    users = MainUser.objects.filter(utoken=utoken)
    goods = MainGoods.objects.filter(productid=goodid)

    u = users.first()
    g = goods.first()

    carts = MainCart.objects.filter(c_user=u).filter(c_goods=g)

    if carts.exists():
        c = carts.first()
        if c.c_num == 1:
            c.delete()
            data['cnum'] = '0'
        else:
            c.c_num = c.c_num - 1
            c.save()
            data['cnum'] = c.c_num

    else:
        data['msg'] = 'fail'
        data['code'] = '703'
        data['desc'] = 'no goods'
    return JsonResponse(data)

#qaun xuan huozhe bu xuan
def allselected(request):
    status = request.GET.get('status')
    utoken = request.COOKIES.get("tokenid")
    users = MainUser.objects.filter(utoken=utoken)
    u = users.first()
    carts = MainCart.objects.filter(c_user=u)
    data = {
        'msg': 'ok',
        'code': '200',
        'desc': 'sucess',

    }
    if status == 'on':
        for cart in carts:
            cart.is_select = False
            cart.save()
        data['select'] = 'select'
    elif status == 'off':
        for cart in carts:
            cart.is_select = True
            cart.save()
        data['select'] = 'noselect'
    return JsonResponse(data)

#chuang jiang ding dan
def create_order(request):
    #huo qu gou wu che zhong de shu ju
    utoken = request.COOKIES.get("tokenid")
    user = MainUser.objects.filter(utoken=utoken)
    u = user.first()
    carts = MainCart.objects.filter(c_user=u).filter(is_select=True)

    order = MainOrder()
    order.o_user = u
    order.o_num = 1
    order.o_status = 1
    order.save()
    deralList = []
    #bian li shu ju
    for cart in carts:
        orderDetail = MainOrderDetail()
        orderDetail.od_order = order
        orderDetail.od_goods = cart
        orderDetail.save()
        deralList.append(orderDetail)
        cart.delete()
    data = {
        'order': order,
        'orderDetail': deralList,
    }
    return render(request, 'order/order.html', context=data)

#gou wu che dan xuan
def selectchange(request):
    gid = request.GET.get('gid')
    carts = MainCart.objects.filter(id=gid)
    cart = carts.first()
    cart.is_select = not cart.is_select
    cart.save()

    data = {
        'code': '200',
        'status': cart.is_select,
        'allselect': True,
    }
    #shi xian dan xuan quan xuan de zhuang tai
    utoken = request.COOKIES.get("tokenid")
    user = MainUser.objects.filter(utoken=utoken)
    u = user.first()
    carts = MainCart.objects.filter(c_user=u)
    if carts.exists():
        for cart in carts:
            if not cart.is_select:
                data['allselect'] = False

    return JsonResponse(data)

#购物车商品增加
def addshopping(request):
    utoken = request.COOKIES.get("tokenid")
    gid = request.GET.get('gid')
    carts = MainCart.objects.filter(id=gid)
    cart = carts.first()
    cart.c_num = cart.c_num + 1
    cart.save()
    data = {
        'code': '200',
        'cnum': cart.c_num,
    }

    return JsonResponse(data)

#购物车商品减少
def subshopping(request):
    utoken = request.COOKIES.get("tokenid")
    gid = request.GET.get('gid')
    carts = MainCart.objects.filter(id=gid)
    cart = carts.first()
    data = {
        'code': '200',
    }
    if cart.c_num == 1:
        cart.delete()
        data['cnum'] = 0
    else:
        cart.c_num = cart.c_num - 1
        data['cnum'] = cart.c_num
        cart.save()
    return JsonResponse(data)


def sumcart(request):
    utoken = request.COOKIES.get("tokenid")
    name = MainUser.objects.filter(utoken=utoken)
    u = name.first()
    carts = MainCart.objects.filter(c_user=u)
    data = {
        'cartsum': 0,
    }
    if carts.exists():
        cartsum = 0
        for cart in carts:
            c = cart.c_num * cart.c_goods.marketprice
            cartsum += c
        cartsum = round(cartsum, 2)
        data['cartsum'] = cartsum
    return JsonResponse(data)
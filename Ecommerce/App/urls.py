from django.conf.urls import url, include
from django.contrib import admin

from App import views

urlpatterns = [
   url(r'^home/', views.home, name='home'),
   url(r'^market/$', views.market, name='market'),
   url(r'^market/(\d+)/(\d+)/(\d+)/(\w+)/(\w+)/', views.marketparam, name='marketparam'),
   url(r'^cart/', views.cart, name='cart'),
   url(r'^mine/', views.mine, name='mine'),
   url(r'^register/', views.user_register, name='register'),
   url(r'^chkuser/', views.chk_username, name='chkuser'),
   url(r'^login/', views.user_login, name='login'),
   url(r'^loginout/', views.user_loginout, name='loginout'),
   url(r'^add_card_num/', views.add_card_num, name='add_card_num'),
   url(r'^sub_card_num/', views.sub_card_num, name='sub_card_num'),
   url(r'^allselected/', views.allselected, name='allselected'),
   url(r'^create/', views.create_order, name='create'),

   #gou wu che dan xuan
   url(r'^selectchange/', views.selectchange, name='selectchange'),
   #zeng jia gou wu che shang pin
   url(r'^addshopping/', views.addshopping, name='addshopping'),
   #jian shao shang pin shu liang
   url(r'^subshopping/', views.subshopping, name='subshopping'),
   #cart zong jia
   url(r'^sumcart/', views.sumcart, name='sumcart'),
   #验证登录
   url(r'^dologin/', views.dologin, name='dologin'),




]
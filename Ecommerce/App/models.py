from django.db import models

class Main(models.Model):
    img = models.CharField(max_length=100)
    name = models.CharField(max_length=25)
    trackid = models.CharField(max_length=20)
    class Meta:
        abstract = True
# Create your models here.
class AppHome( Main ):

    class Meta:
        db_table = 'axf_wheel'


class HomeNav(Main):
    class Meta:
        db_table = 'axf_nav'

class HomeBuy(Main):
    class Meta:
        db_table = 'axf_mustbuy'

class HomeShop(Main):
    class Meta:
        db_table = 'axf_shop'

'''
trackid,name,img,categoryid,brandname,img1,childcid1,productid1,longname1,price1,marketprice1,img2,childcid2,productid2,longname2,price2,marketprice2,img3,childcid3,productid3,longname3,price3,marketprice3
'''
class HomeShow(Main):
    categoryid = models.CharField(max_length=25)
    brandname = models.CharField(max_length=25)
    img1 = models.CharField(max_length=200)
    childcid1 = models.CharField(max_length=25)
    productid1 = models.CharField(max_length=25)
    longname1 = models.CharField(max_length=25)
    price1 = models.FloatField(default=0)
    marketprice1 = models.FloatField(default=0)

    img2 = models.CharField(max_length=200)
    childcid2 = models.CharField(max_length=25)
    productid2 = models.CharField(max_length=25)
    longname2 = models.CharField(max_length=25)
    price2 = models.FloatField(default=0)
    marketprice2 = models.FloatField(default=0)

    img3 = models.CharField(max_length=200)
    childcid3 = models.CharField(max_length=25)
    productid3 = models.CharField(max_length=25)
    longname3 = models.CharField(max_length=25)
    price3 = models.FloatField(default=0)
    marketprice3 = models.FloatField(default=0)

    class Meta:
        db_table = 'axf_mainshow'

'''
axf_foodtypes(typeid,typename,childtypenames,typesort)
'''
#market
class MainMarket(models.Model):
    typeid = models.CharField(max_length=20)
    typename = models.CharField(max_length=20)
    childtypenames = models.CharField(max_length=200)
    typesort = models.IntegerField(default=1)
    class Meta:
        db_table = 'axf_foodtypes'

'''
axf_goods(,,,,,,,,,storenums,productnum) values("11951","http://img01.bqstatic.com/upload/goods/000/001/1951/0000011951_63930.jpg@200w_200h_90Q","","乐吧薯片鲜虾味50.0g",0,0,"50g",2.00,2.500000,103541,103543,"膨化食品","4858",200,4);
'''

class MainGoods(models.Model):
    productid = models.CharField(max_length=25)
    productimg = models.CharField(max_length=200)
    productname = models.CharField(max_length=100)
    productlongname = models.CharField(max_length=100)
    isxf = models.BooleanField(default=False)
    pmdesc = models.IntegerField(default=0)
    specifics = models.CharField(max_length=50)
    price = models.FloatField(default=1)
    marketprice = models.FloatField(default=1)
    categoryid = models.IntegerField(default=0)
    childcid = models.IntegerField(default=0)
    childcidname = models.CharField(max_length=50)
    dealerid = models.CharField(max_length=50)
    storenums = models.IntegerField(default=1)
    productnum = models.IntegerField(default=1)
    class Meta:
        db_table = 'axf_goods'
#yonghu
class MainUser(models.Model):
    name = models.CharField(max_length=25, unique=True)
    email = models.CharField(max_length=25, unique=True)
    phone = models.CharField(max_length=20, unique=True)
    pwd = models.CharField(max_length=200)
    utoken = models.CharField(max_length=32, null=True)
    #False:nan
    gender = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    icon = models.ImageField(upload_to='icons')

class MainCart(models.Model):
    c_user = models.ForeignKey(MainUser)
    c_goods = models.ForeignKey(MainGoods)
    c_num = models.IntegerField(default=1)
    is_delete = models.BooleanField(default=False)
    is_select = models.BooleanField(default=True)

#ding dan

class MainOrder(models.Model):
    o_user = models.ForeignKey(MainUser)
    o_num = models.IntegerField(default=0)
    o_status = models.CharField(default=0, max_length=3)
    o_createtiem = models.DateField(auto_now=True)


# ding dan xiang qing
class MainOrderDetail(models.Model):
    od_goods = models.ForeignKey(MainCart)
    od_order = models.ForeignKey(MainOrder)
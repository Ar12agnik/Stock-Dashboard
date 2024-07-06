from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from .models import stock_info
from main import get_stock_info

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            print("staff!")
            return render(request,'index.html',context={"message":"Please Log out of admin first!!"})
        else:
            stocks = stock_info.objects.filter(user=request.user)
            stock_prices=[]
            total_invested=0
            total_value=0
            for stock in stocks:
                total_invested+=stock.total
                name=stock.symbol
                current_value=get_stock_info(name)*int(stock.no_of_shares)
                total_value+=current_value
                stock.current_price=current_value
                stock.save()
            username=request.user.username
            total_invested=float("{:.2f}".format(total_invested))
            return render(request,'index1.html',context={'stocks':stocks,'total_invested':total_invested,'total_value':total_value,'username':username})
    else:
        if request.method=='POST':
            username=request.POST.get("email")
            passwd=request.POST.get("passwd")
            print(passwd)
            user = authenticate(username=username, password=passwd)
            if user is not None:
                print("loggedin")
                login(request,user)
                return redirect('index')
            else:
                return render(request,'index.html',context={"message":"Invalid Credencials!"})
        else:
            return render(request,'index.html')
@login_required
def logout_user(request):
    logout(request)
    return redirect("index")
@login_required
def add_stock(request):
    if request.method=='POST':
        select=request.POST.get('select')
        flag=1
        if select == 'custom':
            flag=0
            custom=request.POST.get('customSymbol')
        price=float(request.POST.get('price'))
        shares=int(request.POST.get('shares'))
        if flag==1:
            stocks=stock_info.objects.get(user=request.user,symbol=select)
            stocks_price_old=stocks.price
            stocks_quantity_old=stocks.no_of_shares
            stocks_price_old*=stocks_quantity_old
            price*=shares
            price+=stocks_price_old
            print(price)
            shares+=stocks_quantity_old
            avg_price_paid=price/shares
            stocks.price=avg_price_paid
            stocks.total=price
            stocks.flag=1
            stocks.no_of_shares=shares
            stocks.save()
            return redirect("index")
        elif flag==0:
            stock_info.objects.create(symbol=custom,price=price,no_of_shares=shares,user=request.user)
            return redirect("index")
        
            
        
    else:
        stocks = stock_info.objects.filter(user=request.user)
        return render(request,"add_stock.html",context={"stocks":stocks})
@login_required
def add_sell_record(request):
    if request.method=='POST':
        stock=request.POST.get('stock')
        no_of_shares_sold=int(request.POST.get('shares'))
        stocks=stock_info.objects.get(symbol=stock,user=request.user)
        a=stocks.no_of_shares
        if a<no_of_shares_sold:
            stocks = stock_info.objects.filter(user=request.user)
            return render(request,"add_sell_record.html",context={"stocks":stocks,"message":"cannot sell more shares than you own!"})
        else:
            if a-no_of_shares_sold==0:
                stocks.delete()
            else:
                stocks.no_of_shares=int(a)-no_of_shares_sold
                stocks.flag=0
                stocks.save()
            return redirect("index")
    else:
        stocks=stock_info.objects.all()
        
        return render(request,"add_sell_record.html",context={"stocks":stocks})
def detailes(request,pk):
    stock=stock_info.objects.get(id=pk)
    name=stock.symbol
    get_stock_info1=get_stock_info(name)
    current_value=get_stock_info1*int(stock.no_of_shares)
    stock.current_price=current_value
    stock.current_1p=get_stock_info1
    stock.total_invested=stock.price*int(stock.no_of_shares)
    stock.save()
    return render(request,"detailes.html",context={"stocks":stock,"username":request.user})

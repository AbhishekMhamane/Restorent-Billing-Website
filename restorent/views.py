from django.shortcuts import render,redirect
from django.template.response import TemplateResponse
from restorent.models import Customer,Dish,Menu
from datetime import datetime 
from django.contrib import auth
import pytz 
import mysql.connector
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate



def register(request):
    if request.method == "POST":  
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = User.objects.create_user(username=username,password=password)
        user.save()    
        return redirect('/')         
    return render(request,'register.html')  

def login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            request.session['userid']=username
            return redirect('/index')
            
    return render(request,'login.html') 

def logout(request):
    del request.session['userid']
    return redirect('/')





def index(request): 
    if request.session.has_key('userid'):
        print("working")
        menu=Menu.objects.filter(userid=request.session['userid']) 
        if request.method=="POST":
            if request.POST.get('save')=="save":
                name=request.POST.get('customername')
                mobile=request.POST.get('customermobile')
                IST = pytz.timezone('Asia/Kolkata')   
                datetime_ist = datetime.now(IST) 
                t=datetime_ist.strftime('%d/%m/%Y %H:%M %P')
                cust=Customer(userid=request.session['userid'],time=t,name=name,mobile=mobile,amount=0)
                cust.save()
                customer=Customer.objects.get(userid=request.session['userid'],id=cust.id)
        
                n=Menu.objects.all().filter(userid=request.session['userid'])
                total=0
                at=0
                for i in n:
                    at=int(request.POST.get(i.dishname))
                    if at>0:
                        dish=Dish(oid=customer.id,dname=i.dishname,dquantity=at,damount=at*i.dishprice)
                        dish.save()
                        total=total+at*i.dishprice
        
                customer.amount=total  
                customer.save()
                dish=Dish.objects.all().filter(oid=customer.id)
                return render(request,'Recpt.html',{'customer':customer,'dish':dish})
            
        return render(request,'index.html',{'menu':menu,'userdata':request.session['userid']})  
    else :
        return redirect('/')

def show(request):
    if request.session.has_key('userid'):
        customer=reversed(Customer.objects.all().filter(userid=request.session['userid']))
        dish=Dish.objects.all()
        return render(request,'show.html',{'customer':customer,'dish':dish})
    else:
        return redirect('/')

def edit(request,id):
    if request.session.has_key('userid'):
        customer=Customer.objects.get(userid=request.session['userid'],id=id)
        dish=Dish.objects.all().filter(oid=id)
        menu=Menu.objects.all().filter(userid=request.session['userid'])
        l=list()
        ck=0
        for i in menu:
            for j in dish:
                if i.dishname==j.dname:
                    ck=1
                    break
            if ck==0:
                l.append(i.dishname)
            else:
                ck=0
        return render(request,'edit.html',{'customer':customer,'dish':dish,'menu':menu,'list':l})

def update(request,id):
    if request.session.has_key('userid'):
        if request.method == 'POST':
            if request.POST.get('save')=="save":
                customer=Customer.objects.get(userid=request.session['userid'],id=id)
                dish=Dish.objects.all().filter(oid=id) 
                dish.delete()
                name=request.POST.get('customername')
                mobile=request.POST.get('customermobile')
                
                n=Menu.objects.all().filter(userid=request.session['userid'])
                total=0
                at=0
                for i in n:
                    at=int(request.POST.get(i.dishname))      
                    if at>0:
                        dish=Dish(oid=customer.id,dname=i.dishname,dquantity=at,damount=at*i.dishprice)
                        dish.save()
                        total=total+at*i.dishprice
        
        
              
                customer.amount=total  
                customer.name=name
                customer.mobile=mobile
                customer.save()
                return redirect('/show')
        
            if request.POST.get('print')=="print":
                return redirect('/show')
        
        return render(request,'edit.html',{'customer':customer,'dish':dish,'menu':menu})
    else:
        return redirect('/')



def destroy(request,id):
    if request.session.has_key('userid'):
        customer=Customer.objects.get(userid=request.session['userid'],id=id)
        Dish.objects.filter(oid=id).delete()
        customer.delete()
        return redirect('/show')
    else:
        return redirect('/')

def printrp(request,id):
    if request.session.has_key('userid'):
       customer=Customer.objects.get(userid=request.session['userid'],id=id)
       dish=Dish.objects.all().filter(oid=id)
       return render(request,'Recpt.html',{'customer':customer,'dish':dish})
    else:
        return redirect('/')


def additem(request):
    if request.session.has_key('userid'):
        if request.method == "POST":
            userid=request.session['userid']
            dishname=request.POST.get('itemname')
            dishprice=request.POST.get('itemprice')
            dishtype=request.POST.get('itemtype')
            m=Menu(userid=userid,dishname=dishname,dishprice=dishprice,dishtype=dishtype)
            m.save()
            
        return render(request,'additem.html')
    else:
        return redirect('/')


def showitem(request):
    if request.session.has_key('userid'):
        userid=request.session['userid']
        menu=Menu.objects.all().filter(userid=userid)
        return render(request,'showitem.html',{'menu':menu})
    else:
        return redirect('/')

def deleteitem(request,dishname):
    if request.session.has_key('userid'):
        userid=request.session['userid']
        m=Menu.objects.filter(userid=userid,dishname=dishname)
        m.delete()
        return redirect('/showitem')
    else:
        return redirect('/')

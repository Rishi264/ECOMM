from math import ceil

from django.http import HttpResponse
from django.shortcuts import render,redirect

from .models import Product, Contact, Orders, OrderUpdate
import json
import razorpay
from .forms import SignupForm
from django.contrib.auth import login,authenticate


# Create your views here.

def index(request):
    products = Product.objects.all()
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item["category"] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds': allProds}
    return render(request, "shop/index.html", params)

def searchMatch(query, item):
    if query in item.desc.lower() or query in item.product_name.lower():
        return True
    else:
        return False
def search(request):
    query=request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item["category"] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query,item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if(len(prod)!=0):
            allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds': allProds,"msg":""}
    if len(allProds)==0 or len(query)<4:
        params={'msg':"Please make sure to enter relevant search query"}

    return render(request, "shop/search.html", params)


def about(request):
    return render(request,  'shop/about.html')


def contact(request):
    thank =False
    if request.method == "POST":

        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')

        contact=Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
        thank = True
    return render(request, 'shop/contact.html', {'thank': thank})


def tracker(request):
    if request.method=="POST":
        orderId= request.POST.get('orderId', '')
        email= request.POST.get('email', '')

        try:
            order=Orders.objects.filter(order_id=orderId, email=email)

            if len(order)>0:
                update=OrderUpdate.objects.filter(order_id=orderId)
                updates=[]
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response=json.dumps([updates, order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')
    return render(request, 'shop/tracker.html')





def productView(request, id):
    #Fetch the  product using id
    product= Product.objects.filter(id=id)

    return render(request, 'shop/productView.html', {'product': product[0]})


def checkOut(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city, state=state,
                       zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        update=OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkOut.html', {'thank': thank, 'id': id})
        #Request paytm to transfer the amount to your account after payment by user

    return render(request, 'shop/checkOut.html')


a='rzp_test_KpQdWsE3tkC469'
b='jjPsqq1FWPD8MGzJztr7ZTcK'

def pay(request):
    client = razorpay.Client(auth=(a, b))
    order_amount = Orders.objects.all().last().amount * 100
    order_currency = 'INR'

    payment_order=client.order.create(dict(amount=order_amount, currency=order_currency, payment_capture=1))
    payment_order_id=payment_order['id']
    context={
        'amount': Orders.objects.all().last().amount,
        'api_key':a,
        'order_id':payment_order_id

    }
    return render(request, 'shop/pay.html', context)

#signup
def signup(request):
    if request.method=='POST':
        form=SignupForm(request.POST)
        if form.is_valid():

            form.save()
            username=form.cleaned_data.get('username')
            pwd=form.cleaned_data.get('password1')
            user=authenticate(username=username,password=pwd)
            login(request,user)
            return redirect('ShopHome');
    form=SignupForm
    return render(request,'registration/signup.html',{'form':form})

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from orders.models import Topings, Subs, Pizza, Pastas, DP, Salads, orderplaced, orderitems
from django.contrib.auth.decorators import login_required

# Create your views here.
# getting data
@login_required
def menu(request):
    if request.method == "POST":
       pizzaname = request.POST["pizzatype"]
       size = request.POST["pizzasize"]
       toping = request.POST.getlist("topings[]")
       sub = request.POST.getlist("subs")
       pasta = request.POST.getlist("pastas[]")
       salad = request.POST.getlist("salads[]")
       dp = request.POST.getlist("dps[]")
       number = orderitems.objects.last()
       if number == None:
          counter = 1
       else:
          counter = number.order_id + 1
       #orders placed
       yourextras = []
       yourprices = []
       #taking initialprice as zero(0)
       initialpay = 0
       toping_number = len(toping)
#calculating pizza price with topings
       if len(toping) < 6:
           pizza = Pizza.objects.raw('SELECT id, pizza_price FROM orders_pizza WHERE pizza_name = %s AND pizza_type = %s AND pizza_size = %s', [toping_number, pizzaname, size])
           for p in pizza:
               pizzapay = initialpay + p.pizza_price
               yourpizza = "You choose "+p.pizza_type +" Pizza of size " +p.pizza_size+ " with " + p.pizza_name +" topings"
               pizzaadd = orderitems(order_id=counter, items=yourpizza, items_price=p.pizza_price)
               pizzaadd.save()
       else:
           return HttpResponse('select only 5 topings')
#calculating subs price and adding to pizzas price
       subpay = 0
       if len(sub) != 0:
           for i in sub:
               subdue = Subs.objects.raw('SELECT id, subs_price FROM orders_subs WHERE id = %s', [i])
               for s in subdue:
                   subpay = subpay + s.subs_price
                   subadd = orderitems(order_id=counter, items=s.subs_name, items_price=s.subs_price)
                   subadd.save()
                   yoursub = s.subs_name + "--" + s.subs_size
                   yourextras.append(yoursub)
                   yourprices.append(s.subs_price)
#calculating and adding pasta price to calculated price before
       pastapay = 0
       if len(pasta) != 0:
           for i in pasta:
               pastadue = Pastas.objects.raw('SELECT id, pasta_price FROM orders_pastas WHERE id = %s', [i])
               for s in pastadue:
                   pastapay = pastapay + s.pasta_price
                   pastaadd = orderitems(order_id=counter, items=s.pasta_name, items_price=s.pasta_price)
                   pastaadd.save()
                   yourextras.append(s.pasta_name)
                   yourprices.append(s.pasta_price)
#calculating and adding salad price to calculated price before
       saladpay = 0
       if len(salad) != 0:
           for i in salad:
               saladdue = Salads.objects.raw('SELECT id, salad_price FROM orders_salads WHERE id = %s', [i])
               for s in saladdue:
                   saladpay = saladpay + s.salad_price
                   saladadd = orderitems(order_id=counter, items=s.salad_name, items_price=s.salad_price)
                   yourextras.append(s.salad_name)
                   yourprices.append(s.salad_price)
#calculating and adding dinnerplate price to calculated price before
       dpay = 0
       if len(dp) != 0:
           for i in dp:
               dpdue = DP.objects.raw('SELECT id, dp_price FROM orders_dp WHERE id = %s', [i])
               for s in dpdue:
                   dpay = dpay + s.dp_price
                   dadd = orderitems(order_id=counter, items=s.dp_name, items_price=s.dp_price)
                   dadd.save()
                   yourdp = s.dp_name + "--" + s.dp_size
                   yourextras.append(yourdp)
                   yourprices.append(s.dp_price)
#calculating to price to pay
       paydue = pizzapay + subpay + pastapay + saladpay + dpay
       your_order = orderplaced(order_number=counter, order_name=request.user.username, order_price=paydue)
       your_order.save()
       extras = zip(yourextras, yourprices)
       context = {
       "ordernum": counter,
       "pizza": yourpizza,
       "extras": extras,
       "paydue": paydue
       }
       return render(request, "checkout.html", context)

    if request.method == "GET":
        context = {
        "pizzas": Pizza.objects.all(),
        "topings": Topings.objects.all(),
        "smallsub": Subs.objects.raw('SELECT * FROM orders_subs WHERE subs_size="S"'),
        "largesub": Subs.objects.raw('SELECT * FROM orders_subs WHERE subs_size="L"'),
        "pastas": Pastas.objects.all(),
        "salads": Salads.objects.all(),
        "dps": DP.objects.all(),
        "user": request.user.username
        }
        return render(request, "orders.html", context)

@login_required
def myorders(request):
    detail_id = []
    detail_price = []
    detail_status = []
    item_list = []
    user = request.user.username
    for item in orderplaced.objects.raw('SELECT * FROM orders_orderplaced WHERE order_name=%s', [user]):
        order_id = item.order_number
        detail_id.append(order_id)
        order_price = item.order_price
        detail_price.append(order_price)
        status = item.order_status
        detail_status.append(status)
    item_list = [[item.items for item in orderitems.objects.raw('SELECT * FROM orders_orderitems WHERE order_id=%s',[id])] for id in detail_id ]
    order_list = zip(detail_id, detail_price, detail_status, item_list)
    context = {
    "user": user,
    "orders": order_list
    }
    return render(request, "myorders.html", context)

@login_required
def checkout(request):
    id = request.POST["id"]
    user = request.user.username
    res = orderplaced.objects.get(order_name=user, order_number=id)
    res.order_status = "Placed"
    res.save()
    return 	redirect("myorders")

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User 
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from .models import Topping, Pizza, Subs, Salad, Pasta, Dinnerplatter, Cart, Build_pizza, Build_subs, Build_pasta, Build_dinnerplatter, Build_salad, Order
from django.core.mail import send_mail

# Create your views here.

# default route to display menu items
def index(request):
    if not request.user.is_authenticated:
        context = {
            "user": None,
            "message": None 
        }
        return render(request, "orders/login.html", context)
    try:
      customer_cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
      customer_cart = Cart.objects.create(user=request.user)
      customer_cart.total_items = 0
      customer_cart.save()
    context = {
        "user": request.user,
        "total_items": customer_cart.total_items,
        "Pizzas": Pizza.objects.all(),
        "Subs":  Subs.objects.all(),
        "Pastas": Pasta.objects.all(),
        "Salads": Salad.objects.all(),
        "Dinnerplatters": Dinnerplatter.objects.all(),
        "message":None
    }
    return render(request, "orders/menu.html", context)

#route to display subs and give option to add into the cart or go back to shopping other items
def subs(request, subs_id) :
    if not request.user.is_authenticated:
        context = {
            "user": None,
            "message": None 
        }
        return render(request, "orders/login.html", context)
    try:
        s = Subs.objects.get(pk=subs_id)
    except Subs.DoesNotExist:
        raise Http404("This option does not exist") 
    try:
      customer_cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
      customer_cart = Cart.objects.create(user=request.user)
      customer_cart.save()
    context = {
        "user": request.user,
        "total_items": customer_cart.total_items,
        "Subs": s,
        "message":None
    }
    return render(request, "orders/subs.html", context)

#route to display pasta and give option to add into the cart or go back to shopping other items
def pasta(request, pasta_id) :
    if not request.user.is_authenticated:
        context = {
            "user": None,
            "message": None 
        }
        return render(request, "orders/login.html", context)
    try:
        p = Pasta.objects.get(pk=pasta_id)
    except Pasta.DoesNotExist:
        raise Http404("This option does not exist") 
    try:
      customer_cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
      customer_cart = Cart.objects.create(user=request.user)
      customer_cart.save()
    context = {
        "user": request.user,
        "total_items": customer_cart.total_items,
        "Pasta": p,
        "message":None
    }
    return render(request, "orders/pasta.html", context)

#route to display salad and give option to add into the cart or go back to shopping other items

def salad(request, salad_id) :
    if not request.user.is_authenticated:
        context = {
            "user": None,
            "message": None 
        }
        return render(request, "orders/login.html", context)
    try:
        s = Salad.objects.get(pk=salad_id)
    except Salad.DoesNotExist:
        raise Http404("This option does not exist") 
    try:
      customer_cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
      customer_cart = Cart.objects.create(user=request.user)
      customer_cart.save()
    context = {
        "user": request.user,
        "total_items": customer_cart.total_items,
        "Salad": s,
        "message":None
    }
    return render(request, "orders/salad.html", context)

#route to display dinnerplatter and give option to add into the cart or go back to shopping other items
def dinnerplatter(request, dp_id) :
    if not request.user.is_authenticated:
        context = {
            "user": None,
            "message": None 
        }
        return render(request, "orders/login.html", context)
    try:
        s = Dinnerplatter.objects.get(pk=dp_id)
    except Dinnerplatter.DoesNotExist:
        raise Http404("This option does not exist") 
    try:
      customer_cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
      customer_cart = Cart.objects.create(user=request.user)
      customer_cart.save()
    context = {
        "user": request.user,
        "total_items": customer_cart.total_items,
        "Dinnerplatter": s,
        "message":None
    }
    return render(request, "orders/dinnerplatter.html", context)

#route to display pizza along with the available topping options and give option to add into the cart or go back to shopping other items

def pizza(request, pizza_id) :
    if not request.user.is_authenticated:
        context = {
            "user": None,
            "message": None 
        }
        return render(request, "orders/login.html", context)
    try:
        p = Pizza.objects.get(pk=pizza_id)
    except Pizza.DoesNotExist:
        raise Http404("This option does not exist") 
    try:
      customer_cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
      customer_cart = Cart.objects.create(user=request.user)
      customer_cart.save()
    context = {
        "user": request.user,
        "total_items": customer_cart.total_items,
        "Pizza": p,
        "Toppings": Topping.objects.all(),
        "message":None
    }
    return render(request, "orders/pizza.html", context)

#once the customer add subs into the cart, it will ask customer to add more items into the cart or move to checkout.

def add_subs_to_cart(request, subs_id):
    if not request.user.is_authenticated:
        context = {
            "user": None,
            "message": None 
        }
        return render(request, "orders/login.html", context)
    try:
        p = Subs.objects.get(pk=subs_id)
    except Subs.DoesNotExist:
        raise Http404("This option does not exist") 
    try:
        extra_cheese = int(request.POST["extracheese"])
    except:
        extra_cheese = 0

    try:
      customer_cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
      customer_cart = Cart.objects.create(user=request.user)
      customer_cart.save()
    if customer_cart is not None:
      #build subs
      try:
        build_subs = Build_subs.objects.create(substype=p, extracheese=extra_cheese, cart=customer_cart)
        if (build_subs is not None):
          build_subs.save()
        else:
          raise Http404("Subs does not exist") 
      except Build_subs.DoesNotExist:
          raise Http404("Subs does not exist") 
      customer_cart.total_items = customer_cart.totItems()
      customer_cart.total_cost = customer_cart.totCost()

      customer_cart.save()

    context = {
        "customer_cart": customer_cart,
        "user": request.user,
        "total_items": customer_cart.total_items,
        "total_cost": customer_cart.total_cost,
        "message":None
    }
    
    return render(request, "orders/cart.html", context)

#once the customer add pasta into the cart, it will ask customer to add more items into the cart or move to checkout.

def add_pasta_to_cart(request, pasta_id):
    if not request.user.is_authenticated:
        context = {
            "user": None,
            "message": None 
        }
        return render(request, "orders/login.html", context)
    try:
        p = Pasta.objects.get(pk=pasta_id)
    except Pasta.DoesNotExist:
        raise Http404("This option does not exist") 

    try:
      customer_cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
      customer_cart = Cart.objects.create(user=request.user)
    customer_cart.save()
    if customer_cart is not None:
      #build pasta
      try:
        build_pasta = Build_pasta.objects.create(pastatype=p, cart=customer_cart)
        if (build_pasta is not None):
          build_pasta.save()
        else:
          raise Http404("pasta object did not get created")
      except Build_pasta.DoesNotExist:
          raise Http404("Pasta does not exist") 
      build_pasta.save()

      customer_cart.total_items = customer_cart.totItems()
      customer_cart.total_cost = customer_cart.totCost()
      customer_cart.save()

    context = {
        "customer_cart": customer_cart,
        "user": request.user,
        "total_items": customer_cart.total_items,
        "total_cost": customer_cart.total_cost,
        "message":None
    }
    
    return render(request, "orders/cart.html", context)

#once the customer add salad into the cart, it will ask customer to add more items into the cart or move to checkout.

def add_salad_to_cart(request, salad_id):
    if not request.user.is_authenticated:
        context = {
            "user": None,
            "message": None 
        }
        return render(request, "orders/login.html", context)
    try:
        p = Salad.objects.get(pk=salad_id)
    except Salad.DoesNotExist:
        raise Http404("This option does not exist") 

    try:
      customer_cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
      customer_cart = Cart.objects.create(user=request.user)
    customer_cart.save()
    if customer_cart is not None:
      #build salad
      try:
        build_salad = Build_salad.objects.create(saladtype=p, cart=customer_cart)
        if (build_salad is not None):
          build_salad.save()
        else:
          raise Http404("salad object did not get created")
      except Build_salad.DoesNotExist:
          raise Http404("Salad does not exist") 
      build_salad.save()

      customer_cart.total_items = customer_cart.totItems()
      customer_cart.total_cost = customer_cart.totCost()
      customer_cart.save()

    context = {
        "customer_cart": customer_cart,
        "user": request.user,
        "total_items": customer_cart.total_items,
        "total_cost": customer_cart.total_cost,
        "message":None
    }
    
    return render(request, "orders/cart.html", context)

#once the customer add dinnerplatter into the cart, it will ask customer to add more items into the cart or move to checkout.

def add_dinnerplatter_to_cart(request, dp_id):
    if not request.user.is_authenticated:
        context = {
            "user": None,
            "message": None 
        }
        return render(request, "orders/login.html", context)
    try:
        p = Dinnerplatter.objects.get(pk=dp_id)
    except Dinnerplatter.DoesNotExist:
        raise Http404("This option does not exist") 

    try:
      customer_cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
      customer_cart = Cart.objects.create(user=request.user)
    customer_cart.save()
    if customer_cart is not None:
      #build dinnerplatter
      try:
        build_dinnerplatter = Build_dinnerplatter.objects.create(dinnerplattertype=p, cart=customer_cart)
        if (build_dinnerplatter is not None):
          build_dinnerplatter.save()
        else:
          raise Http404("Build_dinnerplatter object did not get created")
      except Build_dinnerplatter.DoesNotExist:
          raise Http404("Dinnerplatter does not exist") 
      build_dinnerplatter.save()

      customer_cart.total_items = customer_cart.totItems()
      customer_cart.total_cost = customer_cart.totCost()
      customer_cart.save()

    context = {
        "customer_cart": customer_cart,
        "user": request.user,
        "total_items": customer_cart.total_items,
        "total_cost": customer_cart.total_cost,
        "message":None
    }
    
    return render(request, "orders/cart.html", context)

#once the customer add pizza into the cart, it will ask customer to add more items into the cart or move to checkout.

def add_to_cart(request, pizza_id):
    if not request.user.is_authenticated:
        context = {
            "user": None,
            "message": None 
        }
        return render(request, "orders/login.html", context)
    try:
        p = Pizza.objects.get(pk=pizza_id)
    except Pizza.DoesNotExist:
        raise Http404("This option does not exist") 
    try:
        topping_list = request.POST.getlist('checklist')
    except:
        topping_list = None 

    if (p.type.type == "cheese"):
       if (len(topping_list) != 0):
         return HttpResponseRedirect(reverse("pizza", args=(pizza_id,)))
    elif (p.type.type == "1 topping"):
       if (len(topping_list) != 1):
         return HttpResponseRedirect(reverse("pizza", args=(pizza_id,)))
    elif (p.type.type == "2 topping"):
       if (len(topping_list) != 2):
         return HttpResponseRedirect(reverse("pizza", args=(pizza_id,)))
    elif (p.type.type == "3 toppings"):
       if (len(topping_list) != 3):
         return HttpResponseRedirect(reverse("pizza", args=(pizza_id,)))
    try:
      customer_cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
      customer_cart = Cart.objects.create(user=request.user)
    customer_cart.save()
    if customer_cart is not None:
      #build pizza
      try:
        build_pizza = Build_pizza.objects.create(pizzatype=p, cart=customer_cart)
        if (build_pizza is not None):
          build_pizza.save()
          for t in topping_list:
            topping_id = int(t)
            try:
              build_pizza.toppings.add(Topping.objects.get(pk=topping_id))
            except Topping.DoesNotExist:
              raise Http404(f"topping {topping_id} does not exist")
        else:
          raise Http404(f"Build_pizza object did not get created") 
      except Build_pizza.DoesNotExist:
          raise Http404("Pizza does not exist") 
      build_pizza.save()

      customer_cart.total_items = customer_cart.totItems()
      customer_cart.total_cost = customer_cart.totCost()
      customer_cart.save()

    context = {
        "customer_cart": customer_cart,
        "user": request.user,
        "total_items": customer_cart.total_items,
        "total_cost": customer_cart.total_cost,
        "message":None
    }
    

    return render(request, "orders/cart.html", context)

#once the customer checkout, it will ask customer to confirm the order. or do more shopping

def checkout(request):
    if not request.user.is_authenticated:
        context = {
            "user": None,
            "message": None 
        }
        return render(request, "orders/login.html", context)
    try:
      customer_cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
      raise Http404("Cart does not exist") 
    context = {
        "customer_cart": customer_cart,
        "user": request.user,
        "total_items": customer_cart.totItems(),
        "total_cost": customer_cart.totCost(),
        "message":None
    }

    return render(request, "orders/checkout.html", context)

#once the customer confirm the order, it will ask customer to place the order or do more shopping

def confirm_order(request):
    if not request.user.is_authenticated:
        context = {
            "user": None,
            "message": None 
        }
        return render(request, "orders/login.html", context)
    try:
      customer_cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
      raise Http404("Cart does not exist") 
    context = {
        "customer_cart": customer_cart,
        "user": request.user,
        "total_items": customer_cart.total_items,
        "total_cost": customer_cart.total_cost,
        "message":None
    }
    return render(request, "orders/confirm_order.html", context)

#once the customer place the order. It creates the order into database and move all the items from the cart to the order. The cart is now empty. The customer will get an email for the order detail and confimations. [Personal touch]

def place_order(request):
    if not request.user.is_authenticated:
        context = {
            "user": None,
            "message": None 
        }
        return render(request, "orders/login.html", context)
    try:
      customer_cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
      raise Http404("Cart does not exist") 
   
    if customer_cart.total_items == 0: 
      return HttpResponse(f"Cart is empty") 

    try:
      customer_order = Order.objects.create(user=request.user)
    except Order.DoesNotExist:
      raise Http404("Error in processing order")

    if customer_cart is not None:
      ordered_pizzas = customer_cart.built_pizzas_in_cart.all()
      customer_order.built_pizzas_in_order.set(ordered_pizzas)
      for piz in ordered_pizzas:
         piz.cart = None 
         piz.save()
      ordered_subs = customer_cart.built_subs_in_cart.all()
      customer_order.built_subs_in_order.set(ordered_subs)
      for sub in ordered_subs:
         sub.cart = None 
         sub.save()
      ordered_salad = customer_cart.built_salad_in_cart.all()
      customer_order.built_salad_in_order.set(ordered_salad)
      for salad in ordered_salad:
         salad.cart = None 
         salad.save()
      ordered_pasta = customer_cart.built_pasta_in_cart.all()
      customer_order.built_pasta_in_order.set(ordered_pasta)
      for pasta in ordered_pasta:
         pasta.cart = None 
         pasta.save()
      ordered_dinnerplatter = customer_cart.built_dinnerplatter_in_cart.all()
      customer_order.built_dinnerplatter_in_order.set(ordered_dinnerplatter)
      for dp in ordered_dinnerplatter:
         dp.cart = None 
         dp.save()
      customer_cart.total_items = customer_cart.totItems() 
      customer_cart.total_cost = customer_cart.totCost() 
      customer_cart.save()

      #extract user email
      email = request.user.email
      #send email to the customer
      customer_order.total_items = customer_order.totItems()
      customer_order.total_cost = customer_order.totCost()
      message = customer_order.order_detail()
      customer_order.save()
      send_mail(
         'Your Order Confirmation',
         message,
         'web50.harvard.vgupta@gmail.com',
         [email],
         fail_silently=False,
      )
 

    context = {
        "user": request.user,
        "order_id": customer_order.id,
        "total_items":customer_cart.total_items,
        "message": "Order is Placed Successfully"
    }
    return render(request, "orders/place_order.html", context)

# When user is asked for login
def login_view(request):
    if request.method == "POST":
      username = request.POST["username"]
      password = request.POST["password"]
      user = authenticate(request, username=username, password=password)
      if user is not None:
          login(request, user)
          return HttpResponseRedirect(reverse("index"))
      else:
          context = {
              "user": None,
              "message": "Invalid credentials." 
          }
          return render(request, "orders/login.html", context)
    context = {
         "user": None,
         "message": None 
    }
    return render(request, "orders/login.html", context)

# When customer logout
def logout_view(request):
    logout(request)
    context = {
        "user": None,
        "message": "Logged out." 
    }
    return render(request, "orders/login.html", context)

# When customer registers 

def register_view(request):
    """User Signup"""
    if request.method == "POST":
       usr = request.POST["username"]
       psw = request.POST["password"]
       psw_repeat = request.POST["password-repeat"]
       try: 
         email= request.POST["email"]
       except KeyError:
         email = None
       try: 
         first_name = request.POST["first_name"]
       except KeyError:
         first_name = None
       try: 
         last_name = request.POST["last_name"]
       except KeyError:
         last_name = None
       if psw != psw_repeat:
         context = {
             "user": None,
             "message": "Password mismatch."
         }
         return render(request, "orders/register.html", context)
       if request.user.is_authenticated:
           return("You are already logged-in as: " +  request.user.username)
       try:
         user = User.objects.get(username=usr)
         if user is None:
          user = User.objects.create_user(usr, email, psw)
          user.save()
          user.first_name = first_name
          user.last_name = last_name
          user.save()
       except User.DoesNotExist:
          user = User.objects.create_user(usr, email, psw)
          user.save()
          user.first_name = first_name
          user.last_name = last_name
          user.save()

       context = {
             "user": user,
             "message": "Register is successfully finished, login now"
       }
       return render(request, "orders/login.html",context)
  
    else:
       context = {
             "user": None,
             "message": None
       }
       return render(request, "orders/register.html", context)

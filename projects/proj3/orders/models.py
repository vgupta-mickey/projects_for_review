from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# possible size offered for any item
class Item_size(models.Model):
 size = models.CharField(max_length=64, unique=True)

 def __str__(self):
   return f"{self.size}"

#topping options to build pizza

class Topping(models.Model):
 type = models.CharField(max_length=64, unique=True)
 def __str__(self):
   return f"{self.type}"
 def __repr__(self):
   return self.__str__()

#pizza categories - regular, sicilian
class Pizza_cat(models.Model):
 cat = models.CharField(max_length=64, unique=True)

 def __str__(self):
   return f"{self.cat}"

#pizza type - 1 topping, 2 topping, 3 topping, special, and cheese
class Pizza_type(models.Model):
 type = models.CharField(max_length=64, unique=True)

 def __str__(self):
   return f"{self.type}"


#all the possible pizzas offered 

class Pizza(models.Model):
    cat = models.ForeignKey(Pizza_cat, on_delete=models.CASCADE, related_name="pizzacategories")
    size = models.ForeignKey(Item_size, on_delete=models.CASCADE, related_name="pizzasizes")
    type = models.ForeignKey(Pizza_type, on_delete=models.CASCADE, related_name="pizzatypes")
    price = models.FloatField()

    class Meta: 
      unique_together = ('cat','size','type',)
   

    def __str__(self):
        return f"{self.cat} {self.size} {self.type} - price ${self.price}"
    def __repr__(self):
        return self.__str__()



# all possible subs types as per menu
class Sub_type(models.Model):
 type = models.CharField(max_length=64, unique=True)

 def __str__(self):
   return f"{self.type}"

# all poosible subs offered 
class Subs(models.Model):
    size = models.ForeignKey(Item_size, on_delete=models.CASCADE, related_name="subsizes")
    type = models.ForeignKey(Sub_type, on_delete=models.CASCADE, related_name="subtypes")
    price = models.FloatField()

    class Meta: 
      unique_together = ('size','type',)
   

    def __str__(self):
        return f"{self.size} {self.type} - price ${self.price}"

# all possible pasta type
class Pasta_type(models.Model):
 type = models.CharField(max_length=64, unique=True)

 def __str__(self):
   return f"{self.type}"

# all possible pasta offered
class Pasta(models.Model):
    type = models.ForeignKey(Pasta_type, unique=True, on_delete=models.CASCADE, related_name="pastatypes")
    price = models.FloatField()


    def __str__(self):
        return f"{self.type} - price ${self.price}"

# all possible salada types
class Salad_type(models.Model):
 type = models.CharField(max_length=64, unique=True)

 def __str__(self):
   return f"{self.type}"

# all possible salad offered
class Salad(models.Model):
    type = models.ForeignKey(Salad_type, unique=True, on_delete=models.CASCADE, related_name="saladtypes")
    price = models.FloatField()


    def __str__(self):
        return f"{self.type} - price ${self.price}"

#all possible Dinnerplatter types
class Dinnerplatter_type(models.Model):
 type = models.CharField(max_length=64, unique=True)

 def __str__(self):
   return f"{self.type}"
# all possible Dinnerplatters offered
class Dinnerplatter(models.Model):
    size = models.ForeignKey(Item_size, on_delete=models.CASCADE, related_name="dinnerplattersizes")
    type = models.ForeignKey(Dinnerplatter_type, on_delete=models.CASCADE, related_name="dinnerplattertypes")
    price = models.FloatField()

    class Meta: 
      unique_together = ('size','type',)
   

    def __str__(self):
        return f"{self.size} {self.type} - price ${self.price}"

#customer cart. each customer will have one cart associated to it. Everytime when a pizza is built out of available pizzas, the instance of that pizza is added into the cart. Cart is a foreignKey to build_pizza instance (many items can belong to the same cart, but the same instance of pizza can't belong to the same cart). The same is applicable to subs, pasta, salad and dinnerplatter. Once customer place the orders, the cart gets empty and all the items belongs to the cart will move into cutomer's order.

class Cart(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE,unique=True)
   total_items = models.IntegerField(default=0)
   total_cost = models.FloatField(default=0)

   def __str__(self):
        return f"{self.user}'s cart has {self.total_items} Items for cost: { self.total_cost}"

   def __repr__(self):
        return self.__str__()

   def totItems(self):
        return self.built_pizzas_in_cart.count() + self.built_subs_in_cart.count() + self.built_pasta_in_cart.count() + self.built_salad_in_cart.count() + self.built_dinnerplatter_in_cart.count();

   def totCost(self):
        tot_cost = 0;
        for pizza in self.built_pizzas_in_cart.all():
           tot_cost += pizza.pizzatype.price
        for subs in self.built_subs_in_cart.all():
           tot_cost += subs.substype.price
           if (subs.extracheese == 1):
             tot_cost += .50 
        for pasta in self.built_pasta_in_cart.all():
           tot_cost += pasta.pastatype.price
        for salad in self.built_salad_in_cart.all():
           tot_cost += salad.saladtype.price
        for dp in self.built_dinnerplatter_in_cart.all():
           tot_cost += dp.dinnerplattertype.price
        return tot_cost;

#customer_order. once customer place a order, a order instance is created and all the items in the customer's cart are moved to the order.


class Order(models.Model):
   user = models.ForeignKey(User, on_delete=models.PROTECT)
   total_items = models.IntegerField(default=0)
   total_cost = models.FloatField(default=0)
   def __str__(self):
        return f"order number: {self.id} belongs to {self.user}"

   def totItems(self):
        return self.built_pizzas_in_order.count() + self.built_subs_in_order.count() + self.built_pasta_in_order.count() + self.built_salad_in_order.count() + self.built_dinnerplatter_in_order.count();

   def totCost(self):
        tot_cost = 0;
        for pizza in self.built_pizzas_in_order.all():
           tot_cost += pizza.pizzatype.price
        for subs in self.built_subs_in_order.all():
           tot_cost += subs.substype.price
           if (subs.extracheese == 1):
             tot_cost += .50 
        for pasta in self.built_pasta_in_order.all():
           tot_cost += pasta.pastatype.price
        for salad in self.built_salad_in_order.all():
           tot_cost += salad.saladtype.price
        for dp in self.built_dinnerplatter_in_order.all():
           tot_cost += dp.dinnerplattertype.price
        return tot_cost;


   def order_detail(self):
     order_info = f"Your Order number is: {self.id}:\n"

     if (self.built_pizzas_in_order.count()):
       order_info += "pizza:"
       for pizza in self.built_pizzas_in_order.all():
          order_info += pizza.__str__() 
          order_info += "\n"
     if (self.built_subs_in_order.count()):
       order_info += "subs:"
       for subs in self.built_subs_in_order.all():
          order_info += subs.__str__() 
          order_info += "\n"
     if (self.built_pasta_in_order.count()):
       order_info += "pasta:"
       for pasta in self.built_pasta_in_order.all():
          order_info += pasta.__str__() 
          order_info += "\n"
     if (self.built_salad_in_order.count()):
       order_info += "salad:"
       for salad in self.built_salad_in_order.all():
         order_info += salad.__str__() 
         order_info += "\n"
     if (self.built_dinnerplatter_in_order.count()):
       order_info += "dinnerplatter:"
       for dinnerplatter in self.built_dinnerplatter_in_order.all():
          order_info += dinnerplatter.__str__() 
          order_info += "\n"

     order_info += f"Total Items: {self.total_items}" 
     order_info += "\n"
     order_info += f"Total Cost: ${self.total_cost}" 
     return order_info


# this class will build pizza based on what customer orders. Each instance of this class belongs to just once customer as the same pizza cannot belong to multple customers. This class has foreignKey relationship to Cart and Order. Until the customer don't place the order, it is associated with customer's cart and once the order is placed the same instance move to the order class.

class Build_pizza(models.Model):
   pizzatype = models.ForeignKey(Pizza, on_delete=models.PROTECT, related_name="total_built_pizzas")
   toppings = models.ManyToManyField(Topping, blank=True, related_name="built_pizzas_with_this_topping")
   cart = models.ForeignKey(Cart, blank=True, on_delete=models.CASCADE, related_name="built_pizzas_in_cart", null=True)
   order = models.ForeignKey(Order, blank=True, on_delete=models.CASCADE, related_name="built_pizzas_in_order", null=True)
    
   def __str__(self):
        return_string = self.pizzatype.__str__()
        return_string +=  "\n"
        #return f"{self.pizzatype} in {self.cart.user}'s cart"
        for topping in self.toppings.all():
            return_string += topping.__str__()
            return_string += "\n"
        return (f"{return_string}")

# this class will build subs based on what customer orders. Each instance of this class belongs to just once customer as the same subs cannot belong to multple customers. This class has foreignKey relationship to Cart and Order classes. Until the customer doesn't place the order, it is associated with the customer's cart and once the order is placed the same instance will move to the order class.

class Build_subs(models.Model):
   substype = models.ForeignKey(Subs, on_delete=models.PROTECT, related_name="total_built_subs")
   cart = models.ForeignKey(Cart, blank=True, on_delete=models.CASCADE, related_name="built_subs_in_cart", null=True)
   order = models.ForeignKey(Order, blank=True, on_delete=models.CASCADE, related_name="built_subs_in_order", null=True)
   extracheese = models.IntegerField(default=0)
   def __str__(self):
        if (self.extracheese == 1):
         return f"{self.substype} with extra cheese"
        else:
         return f"{self.substype}"

# this class will build pasta based on what customer orders. Each instance of this class belongs to just once customer as the same pasta cannot belong to multple customers. This class has foreignKey relationship to Cart and Order classes. Until the customer doesn't place the order, it is associated with the customer's cart and once the order is placed the same instance will move to the order class.

class Build_pasta(models.Model):
   pastatype = models.ForeignKey(Pasta, on_delete=models.PROTECT, related_name="total_built_pasta")
   cart = models.ForeignKey(Cart, blank=True, on_delete=models.CASCADE, related_name="built_pasta_in_cart", null=True)
   order = models.ForeignKey(Order, blank=True, on_delete=models.CASCADE, related_name="built_pasta_in_order", null=True)
    
   def __str__(self):
        return f"{self.pastatype}"

# this class will build salad based on what customer orders. Each instance of this class belongs to just once customer as the same salad cannot belong to multple customers. This class has foreignKey relationship to Cart and Order classes. Until the customer doesn't place the order, it is associated with the customer's cart and once the order is placed the same instance will move to the order class.

class Build_salad(models.Model):
   saladtype = models.ForeignKey(Salad, on_delete=models.PROTECT, related_name="total_built_salad")
   cart = models.ForeignKey(Cart, blank=True, on_delete=models.CASCADE, related_name="built_salad_in_cart", null=True)
   order = models.ForeignKey(Order, blank=True, on_delete=models.CASCADE, related_name="built_salad_in_order", null=True)
    
   def __str__(self):
        return f"{self.saladtype}"

# this class will build dinnerplatter based on what customer orders. Each instance of this class belongs to just once customer as the same  dinnerplatter cannot belong to multple customers. This class has foreignKey relationship to Cart and Order classes. Until the customer doesn't place the order, it is associated with the customer's cart and once the order is placed the same instance will move to the order class.

class Build_dinnerplatter(models.Model):
   dinnerplattertype = models.ForeignKey(Dinnerplatter, on_delete=models.PROTECT, related_name="total_built_dinnerplatter")
   cart = models.ForeignKey(Cart, blank=True, on_delete=models.CASCADE, related_name="built_dinnerplatter_in_cart", null=True)
   order = models.ForeignKey(Order, blank=True, on_delete=models.CASCADE, related_name="built_dinnerplatter_in_order", null=True)
    
   def __str__(self):
        return f"{self.dinnerplattertype} cart"


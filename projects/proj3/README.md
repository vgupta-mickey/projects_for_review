# Project 3

Web Programming with Python and JavaScript

The overall idea of the project is to build a pizza delivery website.

In this project, a customer has to login first before he/she can access the menu of the items they can order online.

The following functions are implemented:

1) User registration 
2) User Login
3) User Logout
4) User gets access to menu once it is logged-in to the website.
5) User will be displayed with all possible items on the website.
6) User clicks on the item he/she is interested to order 
7) once the user clicks on a specific item, it will take the user to a specfic item and will give the user an option to add into the cart.  
8) Once the user add the item into the cart, it will give an option to the user to checkout or do more shopping
9) Once the user checkout, it will ask the user to confirm the order or do more shopping
10) once the user confirms the order, it will ask him/her to place the order or do more shopping.
11)once the order is placed, the cart gets empty for the user and all the items are added into the customer's order.
12) User gets an email for the order confirmation (Pesonal touch)

13) Website owner can manage all the items using admin interface. and it can see the order and order details anytime.


The following artifacts are generated:

1) models.py - The backbone of the website is to define the data model.

First of all I build the menu items using the following tables:

Pizza_cat - Regular or Sicilian
Pizza_type - cheese, 1, 2, 3 toppings or special pizza
Item_size = small and large
Pizza - based on the combination of Pizza_cat, Pizza_type, and Item_size, this table creates all possiblepizza.
Topping - This table contains all possible toppings.
Pizza_build - this table entry gets created based on what customer order. this table choose the pizza from Pizza table and Toppings from topping table. This is added into customer cart. If customer eventually place the order, the Pizza_build objects gets moved from cart to order.

Subs_type - all sub types 
Subs  - based on the combination of Subs_type and Item_size, this table creates all possible subs.
Subs_build - this table entry gets created based on what customer order. this table choose the subs from Subs table. If customer chose to add extra cheese, it will add into the subs. This is added into customer cart. If customer eventually place the order, the Subs_build objects gets moved from cart to order.

The same will be applicable to Pasta, Salad and Dinnerplatter.
Pasta_type, Pasta, Pasta_build
Salad_type, Salad
Dinnerplatter_type, Item_size and Dinnerplatter, Dinnerplatter_build


A single cart is associated to a user. When a user orders an item, it is added into the cart. And the cart will get empty when user place the order.

A order is created for a user when he/she place the order. All the items into the cart will move to the order. The cart gets empty and user can do more shopping and add items into the cart again.

An email is sent to the customer, when the order is placed.

To keep the scope of the project limited, the current website doesn't give an option to delete/remove the items from the cart. Also, this project is not focused on look and feel of the website. 


2) views.py - self explainatory 

main functions - menu, ask to add a item into the cart, checkout, confirm the order, place the order. user registration, login, and logout.
  
3) url.py - self explainatory
4) admin.py - self explanatory 
5) templates/orders - all HTML files
6) static/orders/styles.css - some style to display items on website. 
7) SQLITE database
8) setting for email in settings.py 

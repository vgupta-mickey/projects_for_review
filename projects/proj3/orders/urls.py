from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("pizza/<int:pizza_id>", views.pizza, name="pizza"),
    path("subs/<int:subs_id>", views.subs, name="subs"),
    path("pasta/<int:pasta_id>", views.pasta, name="pasta"),
    path("salad/<int:salad_id>", views.salad, name="salad"),
    path("dinnerplatter/<int:dp_id>", views.dinnerplatter, name="dinnerplatter"),
    path("add_to_cart/pizza/<int:pizza_id>", views.add_to_cart, name="add_to_cart"),
    path("add_to_cart/subs/<int:subs_id>", views.add_subs_to_cart, name="add_subs_to_cart"),
    path("add_to_cart/pasta/<int:pasta_id>", views.add_pasta_to_cart, name="add_pasta_to_cart"),
    path("add_to_cart/salad/<int:salad_id>", views.add_salad_to_cart, name="add_salad_to_cart"),
    path("add_to_cart/dinnerplatter/<int:dp_id>", views.add_dinnerplatter_to_cart, name="add_dinnerplatter_to_cart"),
    path("checkout", views.checkout, name="checkout"),
    path("confirm_order", views.confirm_order, name="confirm_order"),
    path("place_order", views.place_order, name="place_order")
]

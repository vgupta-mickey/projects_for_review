from django.urls import path
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
   path("", views.index, name="index"),
   path("login", auth_views.login, {'template_name': 'lostandfound/login.html'}, name="login"),
   path("logout", auth_views.logout,{'next_page':'index'}, name="logout"),
   path("register", views.register_view, name='register'),
   path("item/<int:type>", views.item_view, name='item'),
   path("search_listings", views.search_listings_view, name='search_listings'),
   path("report_a_lost_item", views.report_a_lost_item_view, name='report_a_lost_item'),
   path("report_a_found_item", views.report_a_found_item_view, name='report_a_found_item'),
   path("display_lost_item/<int:lost_id>", views.display_lost_item_view, name='display_lost_item'),
   path("display_found_item/<int:found_id>", views.display_found_item_view, name='display_found_item'),
   path("contact_for_found_item/<int:lost_id>", views.contact_for_found_item_view, name='contact_for_found_item'),
   path("contact_for_lost_item/<int:found_id>", views.contact_for_lost_item_view, name='contact_for_lost_item'),
   path("search_lost_item_by_cat", views.search_lost_item_by_cat, name='search_lost_item_by_cat'),
   path("search_founnd_item_by_cat", views.search_found_item_by_cat, name='search_found_item_by_cat'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

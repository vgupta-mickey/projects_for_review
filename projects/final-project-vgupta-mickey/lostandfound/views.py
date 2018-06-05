from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, ItemForm
from .models import Address, Item, Lostitem, Founditem, Category
from django.core.mail import send_mail
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector


# Create your views here.

# If a person who lost an item, should search the item on lostandfound site using "I lost an item" option. If a person found an item, should search the item using "i found an item" to see if anybody have reported the item as lost.

listing_options = ['I lost an item', 'I found an item']

# 2 possible tables - 1-lost item table and 2-found item table.
report_type = [1, 2]

# main_page. User will be given the following options:
# search for lost item. search for found item. report a lost item, and report a found item. 

def index(request):
    return render(request, 'lostandfound/main_page.html', {'user': request.user,'options': listing_options, "cat": Category.objects.all()})





#this is called when someone is trying to search a lost item by category
@login_required
def search_lost_item_by_cat(request):
  if request.method == 'POST':
    cat = request.POST["search_list"]
    items = Founditem.objects.filter(item__cat__cat=cat)
    return render(request, 'lostandfound/items_list.html', {'user': request.user,'items_list': items, 'type':report_type[1]})
  else:
    return render(request, 'lostandfound/main_page.html', {'user': request.user,'options': listing_options, "cat": Category.objects.all()})




#this is called when someone is trying to search a lost item by category
@login_required
def search_found_item_by_cat(request):
  if request.method == 'POST':
    cat = request.POST["search_list"]
    items = Lostitem.objects.filter(item__cat__cat=cat)
    return render(request, 'lostandfound/items_list.html', {'user': request.user,'items_list': items, 'type':report_type[0]})
  else:
    return render(request, 'lostandfound/main_page.html', {'user': request.user,'options': listing_options, "cat": Category.objects.all()})



#this is called when someone is trying to search their lost/found items
# the user must be login to the website before they search a lost/found item
@login_required
def search_listings_view(request):
    # Get form information.
 if request.method == 'POST':
    search_method = request.POST["search_list"]
    if search_method == None:
       return Http404("not found")
    try:
        search_input = request.POST["search_input"]
    except ValueError:
        search_input = '' 
    if search_method == 'I lost an item':
        #search item in found list
        if (search_input == ''):
          found_items = Founditem.objects.all()
        else:
          search_words = search_input.split()
          query = SearchQuery(search_words.pop(0))
          for word in search_words:
            query += SearchQuery(word)
          vector = SearchVector('title', 'subCat', 'description')
          found_items = Founditem.objects.filter(item__in=Item.objects.annotate(search=vector).filter(search=query))
        return render(request, 'lostandfound/items_list.html', {'user': request.user,'items_list': found_items, 'type':report_type[1]})
    else:
        #search item in lost list
        if (search_input == ''):
          lost_items = Lostitem.objects.all()
        else:
          search_words = search_input.split() 
          query = SearchQuery(search_words.pop(0))
          for word in search_words:
            query &= SearchQuery(word)

          vector = SearchVector('title', 'subCat', 'description', 'color', )
          lost_items = Lostitem.objects.filter(item__in=Item.objects.annotate(search=vector).filter(search=query))
        return render(request, 'lostandfound/items_list.html', {'user': request.user,'items_list': lost_items, 'type':report_type[0]})

 else:
    return render(request, 'lostandfound/main_page.html', {'user': request.user,'options': listing_options, 'message':None})
   


 
# this is called when someone is reporting a lost item
# the reporter must be login to the website before they register the lost item
@login_required
def report_a_lost_item_view(request):
    return HttpResponseRedirect(reverse("item", args=(report_type[0],)))





# this is called when someone is reporting a found item
# the reporter must be login to the website before they register the lost item
@login_required
def report_a_found_item_view(request):
    return HttpResponseRedirect(reverse("item", args=(report_type[1],)))





# this is called when a new user is signing up to report lost/found item
def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.phone = form.cleaned_data.get('phone')
            user.profile.location = form.cleaned_data.get('location')
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return render(request, 'lostandfound/main_page.html', {'user': request.user,'options': listing_options, 'message':"Thanks for the signup. Please report or search lost/found items"})
    else:
        form = SignUpForm()
    return render(request, 'lostandfound/signup.html', {'form': form})


#this is called when some one wants to report a lost/found item. Also, this is called when soneone submit the form to repoort the lost and found item.

@login_required
def item_view(request, type):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save()
            address = Address.objects.create(street=form.cleaned_data.get('street'),street_no=form.cleaned_data.get('street_no'), city=form.cleaned_data.get('city'), state=form.cleaned_data.get('state'), location_description=form.cleaned_data.get('location_desc'))

            address.save()
            item.location = address
            item.save()
            if type == report_type[0]:
              lost_item = Lostitem.objects.create(user=request.user, item = item)
              lost_item.save()
            elif type == report_type[1]:
              found_item = Founditem.objects.create(user=request.user, item = item)
              found_item.save()
            return render(request, 'lostandfound/main_page.html', {'user': request.user,'options': listing_options, 'message':"The item is saved. Thanks for reporting."})

    else:
        form = ItemForm()
    return render(request, 'lostandfound/item.html', {'form': form, 'report_type': type})

@login_required
def display_lost_item_view(request, lost_id):
        lost_item = Lostitem.objects.get(pk=lost_id)
        return render(request, 'lostandfound/display_item.html', {'item': lost_item, 'type': report_type[0]})





# this is called when someone clicks on a specfic found item.
@login_required
def display_found_item_view(request, found_id):
        found_item = Founditem.objects.get(pk=found_id)
        return render(request, 'lostandfound/display_item.html', {'item': found_item, 'type': report_type[1]})





# this is called when a persom who lost the item click on contact button to contact to the person who reported the same item as found.

@login_required
def contact_for_lost_item_view(request, found_id):
        found_item = Founditem.objects.get(pk=found_id)
        #extract user email
        to_email = found_item.user.email
        #send email to the customer
        message = found_item.emailinfo() 
        message +="\n"
        message += request.user.profile.__str__()
        message += "please contact"
        send_mail(
           'My lost item',
           message,
           'web50.harvard.vgupta@gmail.com',
           [to_email],
           fail_silently=False,
        )
        return render(request, 'lostandfound/main_page.html', {'user': request.user,'options': listing_options, 'message':"An email is sent to person who reported the item as found"})




# this is called when a person who found the item click on contact button to contact to the person who reported the same item as lost.

@login_required
def contact_for_found_item_view(request, lost_id):
        lost_item = Lostitem.objects.get(pk=lost_id)
        #extract user email
        to_email = lost_item.user.email
        #send email to the customer
        message = lost_item.emailinfo() 
        message +="\n"
        message += request.user.profile.__str__()
        message += "please contact"
        send_mail(
           'found item',
           message,
           'web50.harvard.vgupta@gmail.com',
           [to_email],
           fail_silently=False,
        )
        return render(request, 'lostandfound/main_page.html', {'user': request.user,'options': listing_options, 'message':"An email is sent to person who reported the item as lost"})

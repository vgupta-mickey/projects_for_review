from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

# extended the user account with phone number, so that people can contact to each other using phone number.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10,blank=True)

    def __str__(self):
        info = f"my name: {self.user.first_name} {self.user.last_name} \n"
        info += f"my phone: {self.phone}\n"
        info += f"my email: {self.user.email}\n"
        return info;



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


#Item category such as electronics, jewellery, clothing etc. This must be pre-populated into the database. All the possible categories must be created for the items in database. 

class Category(models.Model):
   cat = models.CharField(max_length=100, unique=True)
   def __str__(self):
        return f"{self.cat}"

#This class stores the address/location of the item reported by a user.
class Address(models.Model):
  street = models.CharField(max_length=128, blank=True)
  street_no = models.CharField(max_length=16, blank=True, null=True)
  city = models.CharField(max_length=16, blank=False, null=False)
  state = models.CharField(max_length=16, blank=False, null=False)
  location_description = models.TextField(blank=True, null=True)

  def __str__(self):
        return f"{self.street_no} {self.street} {self.city} {self.state}"

#This class is to store the lost/found item info and location.

class Item(models.Model):
   cat = models.ForeignKey(Category, blank=False, on_delete=models.CASCADE, related_name="allitems")
    
   subCat = models.CharField(max_length=64, blank=False)

   date = models.DateField(null=True)

   location = models.ForeignKey(Address, blank=True, null=True, on_delete=models.CASCADE, related_name="allitems")

   color = models.CharField(max_length=64, blank=False)

   title = models.CharField(max_length=128, blank=False)

   description = models.TextField(blank=False)
 
   picture = models.ImageField(blank=True)


   def __str__(self):
        return f"{self.title} {  self.color  } {self.location}"

#This  class maintain the lost items list and who reported the item

class Lostitem(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   item = models.OneToOneField(Item, blank=False, on_delete=models.CASCADE)
   def __str__(self):
        return f" lost Item: {self.item.id} reported by {self.user}"

   def emailinfo(self):
        return f" You have reported this item as lost -- {self.item}\n"
   
#This  class maintain the found items and who reported them.
class Founditem(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   item = models.OneToOneField(Item, blank=False, on_delete=models.CASCADE)

   def __str__(self):
        return f" found Item: {self.item.id} reported by {self.user}"

   def emailinfo(self):
        return f" You have reported this item as found -- {self.item}\n"


# final-project

Project goals and objectives:

It is not unusual that we loose our stuffs at public places and it is highly unlikely that we can trace them back unless we all work together and help each other. With this goal in mind, I decided to build a lostandfound website.

The webiste is design with the following high level user requirements:

1. Website should allow users to report a lost item 
2. Website should allow users to report a found item
3. User must be logged-in before they can report  a lost/found item
4. If user doesn't have an account, they should be allowed to create one with email and phone number.
5. Users should be allowed to search their lost/found items on website using few key words [full search]
6. User should be allowed to search based on item category.
7. If user think that the item they are searching for is listed on the website and wants to contact to the party, they should have an option to send email.
8. When user search for the item, the item details and the location of item where it found/lost should be displayed on google map. [google map integration]  
9. The site should be dynamic and should respond across various devices 


I experimented the following new ideas as a part of this project:

1. I used Django forms
2. I used Django in-build login/logout/ registation forms
3. I extended user account with additional user info - phone number
4. I used postgress full search algorithm to search item based on few key words. The full search is  done on one of the following fields : title, description, category and subCategory.
5. I also used Django forms and models to display item forms to user.
6. I also integrated google map to display item location on google map.
7. I used external database - postgress on Heruko instead of sqlite. The various posible categories of items must be created in database before the site goes online.


Here is how the website will work:

1. When user enters 127.0.0.1:8000,  it will take the user to website main page where user will be given with various search options to search their lost/found items. The main page also allow user to report a lost or found item.

2. If user clicks any of the options in the main page, he/she will be redirected to login if they are already not logged-in. User will have an option to create user profile if he/she has not created yet.

3. Once user is logged-in, we will be redirected to the main page. 

3. If a user found an item and wants to see if somebody on the website has reported the item as lost, he can choose to search item by selecting "I found item" and enter some key words about the items. Similarily for "I lost item".

4. If there is a match for the item in the database, it displays all the items matches the search words. 
   It is recommended to start a search with common one or two words.

5. once a user is listed with possible items, the user should click one of the items which matches the item he/she found.

6. On click on a specific item, item will be described in detail with the item picture if it was uploaded and the location of the item on google map if it is a valid address.  

7. User will be given an option to contact the person so that the lost/found item can be claimed.

8. The same will work for rest  of other options and its pretty self explanatory.
 

Aritifacts :


Its Django web framework and it is very self explanatory. An external database (postgress) is used for the project. A new file forms.py is added to use Django forms framework for creating forms for login/logout/registrations/to report lost and found items. 

settings.py will have MEDIA setting for image uploads. Also new python module pillow is installed for the same purpose.

views.py, urls.py, admin.py, model.py are very self explainatory.


Let me exmplain the models for the lost and found project:


1. A profile class is created which is derived from user class to add phone number as a part of user profile.

2.  Every lost and found item must be given category. So a category Table is created to create possible categories for all possible items.

3. An Address table is created to report lcoation of the lost/found item.

4. An Item is created which can be lost or found item.

5. A separate table Lostitem for lost items are created which will have onetoone relationship with an item and will be associated with an user.

5. A separate table Founditem for lost items are created which will have onetoone relationship with an item and will be associated with an user.


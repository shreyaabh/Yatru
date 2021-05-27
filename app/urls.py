from django.urls import path
from app import views
app_name = 'app'
urlpatterns = [
    path('login/',views.loginuser,name='loginuser'),
    path('signup/',views.signupuser,name='signupuser'),
    path('logout/',views.logoutuser,name='logoutuser'),
    path('', views.home,name='home'),
    path('myprofile/', views.my_profile_view, name='my-profile-view'),
    path('new-messages/',views.new_messages,name='new_messages'),
    path('view-messages/',views.view_messages,name='view_messages'),
    path('delete-messages/',views.delete_messages,name='delete_messages'),
]
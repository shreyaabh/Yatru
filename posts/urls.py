from django.urls import path
from posts import views

app_name = 'posts'
urlpatterns = [
    path('',views.post_views,name='post_views'),
    path('liked/',views.like_unlike,name='like_unlike'),
    path('add-post/',views.post_add,name='post_add'),
    path('search/',views.search,name='search'),
    

]
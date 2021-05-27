from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from .models import Post,Like
from app.models import Yatru
from .forms import PostModelForm
from django.contrib.auth.models import User
import folium,geocoder
# Create your views here.

def post_views(request):
    qs = Post.objects.all()
    context = {
        'qs':qs,
    }

    return render(request,'posts/main.html',context)

def post_add(request):
    
    form = PostModelForm(request.POST,instance=Post())
    if request.method == 'POST':
        newpost=form.save()
        newpost.user=request.user
        newpost.save()
        
    return render(request, 'posts/my_post.html', {'form':PostModelForm()})


def like_unlike(request):
    user = request.user 
    if request.method == 'POST':
        location_post_id = request.POST.get('location_post_id')
        location_obj = Post.objects.get(id=location_post_id)
        profile = Yatru.objects.get(user=user)

        if profile in location_obj.liked.all():
            location_obj.liked.remove(profile)
        else:
            location_obj.liked.add(profile)
        
        like, created = Like.objects.get_or_create(user=profile, location_post_id=location_post_id)

        if not created:
            if like.value=='Like':
                like.value='Unlike'
            else:
                like.value='Like'
            
            location_obj.save()
            like.save()
    return redirect('posts:post_views')
########################################################
# def search(request):  
#     query=request.GET.get('query')
#     query=query.upper()
#     if Post.objects.filter(location=query).exists():
#         allPosts= Post.objects.filter(location=query)
#         params={'allPosts': allPosts}
#         return render(request, 'posts/search.html', params)
#     else:
#         return render(request, 'posts/search.html', {'error':'The keyword you entered not found. You can try the advance search below!'})
########################################################

def search(request): 
    qs = Post.objects.all()
    location_query= request.GET.get('location')
    details_query= request.GET.get('details')
    user_query= request.GET.get('user')
    days_query= request.GET.get('days')
    people_query= request.GET.get('people')
    date_query= request.GET.get('date')
    gender_query= request.GET.get('gender')

    if location_query !='' and location_query is not None:
        qs=qs.filter(location__icontains=location_query)

    elif details_query !='' and details_query is not None:
        qs=qs.filter(detail__icontains=details_query)

    elif user_query !='' and user_query is not None:
        qs=qs.filter(author__icontains=user_query)

    elif days_query !='' and days_query is not None:
        qs=qs.filter(no_days__icontains=days_query)

    elif people_query !='' and people_query is not None:
        qs=qs.filter(no_people__icontains=people_query)

    elif date_query !='' and date_query is not None:
        qs=qs.filter(tour_date__icontains=date_query)

    elif gender_query !='' and gender_query is not None:
        qs=qs.filter(Gender_prefer__icontains=gender_query)
    ##########################################################
    address='Kathmandu'
    location=geocoder.osm(address)
    lat=location.lat 
    lng=location.lng
    country=location.country
    m=folium.Map(height=500,location=[28, 84], zoom_start=7)
    folium.Marker([lat,lng],popup=country).add_to(m)
    m=m._repr_html_()  
    ##########################################################
    context = {
        'qs':qs,
        'm':m,
    }
    return render(request, 'posts/search.html',context)




    

    
  
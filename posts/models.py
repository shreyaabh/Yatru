from django.db import models
from django.core.validators import FileExtensionValidator #to validate the type of image
from app.models import Yatru
from datetime import timezone

# Create your models here.
class Post(models.Model):
    no_people = models.IntegerField()
    no_days = models.IntegerField()
    tour_date = models.DateField()
    Gender_types = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    )
    Gender_prefer = models.CharField(max_length=6, choices=Gender_types)
    location = models.CharField(max_length=200, blank=True)
    pic_location = models.ImageField(blank=True, upload_to="posts/")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    detail = models.TextField() 
    liked = models.ManyToManyField(Yatru, blank=True, related_name= 'likes')
    author = models.ForeignKey(Yatru, on_delete=models.CASCADE, related_name = 'posts',blank=True)

    def __str__(self):
        return str(self.location)

    def no_likes(self):
        return self.liked.all().count()
    
    class Meta:
        ordering = ('-created',)

    def save(self, *args, **kwargs):
        self.location = self.location.upper()
        return super(Post, self).save(*args, **kwargs)

LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)

class Like(models.Model): 
    user = models.ForeignKey(Yatru, on_delete=models.CASCADE)
    location_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user}-{self.location_post}-{self.value}"
    def total_likes(self):
        return self.likes.count()
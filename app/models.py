from django.db import models
from django.contrib.auth.models import User
from .utils import code_generator
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.urls import reverse



# Create your models here.
class Yatru(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True)
    bio = models.TextField(max_length=300)
    Gender_types = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others'),
    )
    Gender = models.CharField(max_length=1, choices=Gender_types)
    email = models.EmailField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(blank=False, upload_to="avatars/")
    friends = models.ManyToManyField(User, blank=True, related_name="friends")
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def get_friends(self):
        return self.friends.all()

    def get_friends_no(self):
        return self.friends.all().count()

    def get_posts_no(self):
        return self.friends.all().count()

    def get_all_authors_posts(self):
        return self.posts.all().count()

    def get_likes_given_no(self):
        likes = self.like_set.all()
        total_liked = 0
        for content in likes:
            if content.value == 'Like':
                total_liked += 1
        return total_liked

    def get_likes_recieved_no(self):
        posts = self.like_set.all()
        total_liked = 0
        for content in posts:
                total_liked += content.likes.all().count()
        return total_liked


    
 
    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%d-%m-%Y')}"

    def save(self, *args, **kwargs):
        ex = False
        if self.first_name and self.last_name:
            to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
            ex = Yatru.objects.filter(slug=to_slug).exists()
            while ex:
                    to_slug = slugify(to_slug + " " + str(code_generator()))
                    ex = Yatru.objects.filter(slug=to_slug).exists()
        else:
            to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)


# class RelationshipManager(models.Manager):
#     def invatations_received(self, receiver):
#         qs = Relationship.objects.filter(receiver=receiver, status='send')
#         return qs


class Relationship(models.Model):
    sender = models.ForeignKey(Yatru, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Yatru, on_delete=models.CASCADE, related_name='receiver')
    STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"

class Message(models.Model):
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiver", null=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.author} Message to {self.receiver}'

    def get_absolute_url(self):
        return reverse("date-page")
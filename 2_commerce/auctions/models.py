from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields.related import RECURSIVE_RELATIONSHIP_CONSTANT


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank=True)

class Listing(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    is_open = models.BooleanField(default=True)
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.FloatField()
    current_bid = models.FloatField(default=0.0)
    current_winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image_url = models.URLField(null=True)
    category = models.CharField(null=True, max_length=64)
    def __str__(self):
        return f"{self.title} (R$ {self.starting_bid})"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()

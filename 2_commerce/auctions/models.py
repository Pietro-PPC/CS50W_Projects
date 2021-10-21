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
    minimum_bid = models.FloatField()
    image_url = models.URLField(null=True, blank=True)
    category = models.CharField(max_length=64, null=True, blank=True)
    def __str__(self):
        return f"{self.title} (US$ {self.minimum_bid})"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_bids')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listing_bids')
    value = models.FloatField(default=0.0)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    product = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200, blank=True)
    lister = models.CharField(max_length=64)
    product_image = models.ImageField(null=True, blank=True, upload_to="images/")
    image_url = models.URLField(null=True, blank=True)
    category = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return f"{self.product} : ${self.price}"
 

class Bid(models.Model):
    bid = models.DecimalField(max_digits=12, decimal_places=2)
    bidder = models.ForeignKey(User, related_name="bids", on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Listing, on_delete=models.CASCADE,)

    def __str__(self):
        return f"{self.bidder} bids for {self.bid} on {self.product}"


class Comment(models.Model):
    comment_text = models.TextField(max_length=200)
    commenter = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Listing, on_delete=models.CASCADE,)

    def __str__(self):
        return f"{self.commenter} comments on {self.product}"


class Watchlist(models.Model):
    watchlist = models.BooleanField(default=False)
    user = models.ForeignKey(User, related_name="watchlist", on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} added {self.product} to watchlist"
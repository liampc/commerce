from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment
from .forms import Add_listing


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def listings(request, product_id):
    bids = Bid.objects.filter(product=product_id)
    if request.method == "POST" and request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        listing = Listing.objects.get(pk=product_id)
        newbid = Bid.objects.create(bid=int(request.POST['bid_price']), bidder=user, product=listing)
        return render(request, "auctions/listings.html", {
            "listing": listing,
            "bids": f"{bids.count()}",
            "newbid": f"{newbid.bid}"
        })

    return render(request, "auctions/listings.html", {
        "listing": Listing.objects.get(id=product_id),
        "bids": f"{bids.count()}",
        "comments": Comment.objects.filter(id=product_id)
    })


def add_listing(request):
    if request.method == "POST":
        form = Add_listing(request.POST)
        if form.is_valid():
            new = Listing()
            new.product = form.cleaned_data["product"]
            new.price = form.cleaned_data["price"]
            new.description = form.cleaned_data["description"]
            new.lister = request.user.id
            new.save()
            return render(request, "auctions/add_listing.html", {
                "message": "Your Listing has been added!"
            })
    
    return render(request, "auctions/add_listing.html", {
        "form": Add_listing()
    })
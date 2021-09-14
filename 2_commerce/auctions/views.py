from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Comment
from . import page_forms


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all().filter(is_open=True)
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

def new_listing(request):
    print(request.user)
    if request.method == 'POST':
        form = page_forms.NewListingForm(request.POST)
        if form.is_valid():
            l = Listing(
                creator=request.user,
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                starting_bid=form.cleaned_data["starting_bid"],
                category=form.cleaned_data["category"],
                image_url=form.cleaned_data["url"]
            )
            l.save()
            return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/new_listing.html", {
        "form": page_forms.NewListingForm()
    })

def listing_page(request, id):
    try:
        listing = Listing.objects.get(pk=id)
    except Listing.DoesNotExist:
        return HttpResponse("This listing does not exist!")

    min_bid = max(listing.current_bid, listing.starting_bid)

    bid_error = False
    if request.method == "POST":
        bid = request.POST.get("bid")
        text = request.POST.get("text")
        if bid:
            if float(bid) >= listing.starting_bid and float(bid) > listing.current_bid:
                listing.current_bid = bid
                listing.current_winner = request.user
                listing.save()
                min_bid = bid
            else:
                bid_error = True
        elif text:
            comment = Comment(
                user=request.user,
                listing=listing,
                text=text
            )
            comment.save()
    
    comments = Comment.objects.all().filter(listing__id=id)
    print(comments)
    watchlist = []
    if request.user.is_authenticated:
        watchlist = request.user.watchlist.all()
    
    return render(request, "auctions/listing_page.html", {
        'listing': listing,
        'watchlist': watchlist,
        'min_bid': min_bid,
        'bid_error': bid_error,
        'comments': comments
    })

def toggle_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = request.user
    if listing not in user.watchlist.all():
        user.watchlist.add(listing)
    else:
        user.watchlist.remove(listing)
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))

def close_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.is_open=False
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))

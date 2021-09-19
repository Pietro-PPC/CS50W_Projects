from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max

from .util import getCurrentBid, getListingsBids

from .models import User, Listing, Comment, Bid
from . import page_forms


def index(request):
    """
    Main page - Active listings
    """
    listings = Listing.objects.all().filter(is_open=True)
    return render(request, "auctions/index.html", {
        "listings": getListingsBids(listings)
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
    if request.method == 'POST':
        form = page_forms.NewListingForm(request.POST)
        if form.is_valid():
            l = Listing(
                creator=request.user,
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                minimum_bid=form.cleaned_data["minimum_bid"],
                category=form.cleaned_data["category"],
                image_url=form.cleaned_data["url"]
            )
            l.save()
            return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/new_listing.html", {
        "form": page_forms.NewListingForm()
    })

def listing_page(request, id):
    # Tests if listing page requested exists
    try:
        listing = Listing.objects.get(pk=id)
    except Listing.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))

    current_bid = getCurrentBid(listing)

    bid_error = False
    if request.method == "POST":
        bid = request.POST.get("bid")
        text = request.POST.get("text")
        if bid:
            bid = float(bid)
            if (current_bid is None and bid >= listing.minimum_bid) or bid > current_bid.value:
                new_bid = Bid(
                    user = request.user,
                    listing = listing,
                    value = bid
                )
                new_bid.save()
                min_bid = bid
                current_bid = new_bid
            else:
                bid_error = True
        elif text:
            comment = Comment(
                user=request.user,
                listing=listing,
                text=text
            )
            comment.save()
    
    min_bid = listing.minimum_bid if not current_bid else current_bid.value
    comments = listing.comments.all()

    return render(request, "auctions/listing_page.html", {
        'listing': listing,
        'min_bid': min_bid,
        'bid_error': bid_error,
        'comments': comments,
        'current_bid': current_bid
    })

def toggle_watchlist(request, listing_id):
    """
    Toggles if listing is in user's watchlist
    """
    listing = Listing.objects.get(pk=listing_id)
    user = request.user
    if listing not in user.watchlist.all():
        user.watchlist.add(listing)
    else:
        user.watchlist.remove(listing)
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))

def close_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    # Closes only if the requester is the owner
    if listing.creator == request.user:
        listing.is_open=False
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))
    return HttpResponseRedirect(reverse("index"))

def watchlist(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    return render (request, "auctions/watchlist.html", {
        'watchlist': getListingsBids(user.watchlist.all())
    })

def categories(request):
    """
    Page with all the categories with open listings
    """
    # Gets a list of all the categories with open listings
    categories = Listing.objects.filter(is_open=True).values_list('category', flat=True)
    categories = categories.distinct().order_by('category')
    
    return render(request, "auctions/categories.html", {
        'categories': categories
    })

def category(request, cat):
    """
    Page with all open listings within category cat
    """
    listings = Listing.objects.all().filter(category=cat)
    if (len(listings) == 0):
        return HttpResponse("A categoria não existe!")

    listings = listings.filter(is_open=True)
    return render(request, "auctions/category.html", {
        'category': cat,
        'listings': getListingsBids(listings)
    })
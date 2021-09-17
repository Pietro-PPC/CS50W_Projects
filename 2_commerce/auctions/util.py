from .models import Bid, Listing
from django.db.models import Max

def getCurrentBid(listing):
    current_bid = None
    listing_bids = listing.listing_bids.all()
    if len(listing_bids) > 0:
        current_bid = listing_bids.order_by('-value').first()
    return current_bid

def getListingsBids(listings):
    listings_bids = []
    for listing in listings:
        newElement = {
            'listing': listing,
            'cur_bid': listing.listing_bids.aggregate(Max('value'))["value__max"]
        }
        listings_bids.append(newElement)
        
    return listings_bids
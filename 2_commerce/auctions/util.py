def getCurrentBid(listing):
    current_bid = None
    listing_bids = listing.listing_bids.all()
    if len(listing_bids) > 0:
        current_bid = listing_bids.order_by('-value').first()
    return current_bid
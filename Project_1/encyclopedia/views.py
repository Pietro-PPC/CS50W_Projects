from django.shortcuts import render
from django.http import HttpResponse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wikiPage(request, page):
    entry = util.get_entry(page)
    if entry == None:
        return HttpResponse(f"Page not found!")
    else:
        return HttpResponse(f"{entry}")
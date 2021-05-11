from markdown2 import markdown

from django.shortcuts import render
from django.http import HttpResponse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wikiPage(request, page):
    content = util.get_entry(page)
    if content == None:
        return HttpResponse(f"Page not found!")
    else:
        content = markdown(content)
        return render(request, "encyclopedia/page.html", {
            "page": page,
            "content": content
        })
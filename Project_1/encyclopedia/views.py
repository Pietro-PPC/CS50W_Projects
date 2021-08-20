from markdown2 import markdown
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django import forms
from . import util

class searchPageForm(forms.Form):
    page = forms.CharField(label="page")

def wikiPage(request, page):
    content = util.get_entry(page)
    if content == None:
        return HttpResponse(f"Page not found!")
    else:
        content = markdown(content)
        return render(request, "encyclopedia/page.html", {
            "form": searchPageForm(),
            "page": page,
            "content": content
        })

def searchPage(request):
    if request.method == 'POST':
        form = searchPageForm(request.POST)
        
        if form.is_valid():
            query_page = form.cleaned_data["page"]
            page = util.get_entry(query_page)
            if page != None:
                return HttpResponseRedirect(reverse("encyclopedia:wikipage", args=[query_page]))

    return HttpResponseRedirect(reverse("encyclopedia:index"))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "form": searchPageForm(),
        "entries": util.list_entries()
    })
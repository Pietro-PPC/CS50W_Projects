from markdown2 import markdown
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django import forms
from . import util

import random

class searchPageForm(forms.Form):
    page = forms.CharField(label="page")

class PageForm(forms.Form):
    name = forms.CharField(label="name")
    body = forms.CharField(label="body", widget=forms.Textarea)

class EditPageForm(forms.Form):
    body = forms.CharField(label="", widget=forms.Textarea)

def notFound(request):
    return HttpResponse("Page not found!")

def wikiPage(request, page):
    content = util.get_entry(page)
    if content == None:
        return HttpResponseRedirect(reverse('encyclopedia:notfound'))
    else:
        content = markdown(content)
        return render(request, "encyclopedia/page.html", {
            "form": searchPageForm(),
            "page": page,
            "content": content
        })


def getSimilarEntries(query_page):
    """
        Returns pages which have query_page as a substring
    """
    similar_entries = []
    pages = util.list_entries()

    for p in pages:
        if query_page in p:
            similar_entries.append(p)

    return similar_entries

def searchPage(request):
    if request.method == 'POST':
        form = searchPageForm(request.POST)
        if form.is_valid():

            query_page = form.cleaned_data["page"]
            page = util.get_entry(query_page)
            if page != None:
                return HttpResponseRedirect(reverse("encyclopedia:wikipage", args=[query_page]))
            else:
                return render(request, "encyclopedia/searchPage.html", {
                    "form": searchPageForm(),
                    "query": query_page,
                    "results": getSimilarEntries(query_page)
                })
    return HttpResponseRedirect(reverse("encyclopedia:index"))

def editPage(request, page):

    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            util.save_entry(page, form.cleaned_data["body"])
            return HttpResponseRedirect(reverse("encyclopedia:wikipage", args=[page]))

    body = util.get_entry(page)
    if body != None:
        return render (request, "encyclopedia/editPage.html", {
            "form": searchPageForm(),
            "page": page,
            "editpageform": EditPageForm(initial={"body": body})
        })
    else:
        return HttpResponseRedirect('notfound')

def newPage(request):
    error = False
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            body = form.cleaned_data["body"]

            if util.get_entry(name) == None:
                util.save_entry(name, body)
                return HttpResponseRedirect(reverse("encyclopedia:wikipage", args=[name]))
            else:
                error = True
    
    return render(request, "encyclopedia/createPage.html", {
        "form": searchPageForm(),
        "newpageform": PageForm(),
        "error": error
    })

def randomPage(request):
    pages = util.list_entries()
    random.seed()
    page = pages[random.randrange(len(pages))]
    return HttpResponseRedirect(reverse("encyclopedia:wikipage", args=[page]))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "form": searchPageForm(),
        "entries": util.list_entries()
    })
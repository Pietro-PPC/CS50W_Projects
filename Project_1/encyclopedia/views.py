from markdown2 import markdown
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django import forms
from . import util

import random

class SearchPageForm(forms.Form):
    page = forms.CharField(label="Search page",
        widget=forms.TextInput(attrs={'placeholder':'Page title here...'}))

class PageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content", widget=forms.Textarea)

class EditPageForm(forms.Form):
    content = forms.CharField(label="Content", widget=forms.Textarea)

def notFound(request):
    return render(request, "encyclopedia/notFoundPage.html", {
        "form": SearchPageForm()
    })

def wikiPage(request, page):
    content = util.get_entry(page)
    if content == None:
        return HttpResponseRedirect(reverse('encyclopedia:notfound'))
    else:
        content = markdown(content)
        return render(request, "encyclopedia/page.html", {
            "form": SearchPageForm(),
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
        form = SearchPageForm(request.POST)
        if form.is_valid():

            query_page = form.cleaned_data["page"]
            page = util.get_entry(query_page)
            if page != None:
                return HttpResponseRedirect(reverse("encyclopedia:wikipage", args=[query_page]))
            else:
                return render(request, "encyclopedia/searchPage.html", {
                    "form": SearchPageForm(),
                    "query": query_page,
                    "results": getSimilarEntries(query_page)
                })
    return HttpResponseRedirect(reverse("encyclopedia:index"))

def editPage(request, page):

    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            util.save_entry(page, form.cleaned_data["content"])
            return HttpResponseRedirect(reverse("encyclopedia:wikipage", args=[page]))

    content = util.get_entry(page)
    if content != None:
        return render (request, "encyclopedia/editPage.html", {
            "form": SearchPageForm(),
            "page": page,
            "editpageform": EditPageForm(initial={"content": content})
        })
    else:
        return HttpResponseRedirect('notfound')

def newPage(request):
    error = False
    entryForm = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            if util.get_entry(title) == None:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("encyclopedia:wikipage", args=[title]))
            else:
                error = True
                entryForm = PageForm(initial={"title": title, "content": content})
    
    return render(request, "encyclopedia/createPage.html", {
        "form": SearchPageForm(),
        "newpageform": entryForm,
        "error": error
    })

def randomPage(request):
    pages = util.list_entries()
    random.seed()
    page = pages[random.randrange(len(pages))]
    return HttpResponseRedirect(reverse("encyclopedia:wikipage", args=[page]))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "form": SearchPageForm(),
        "entries": util.list_entries()
    })
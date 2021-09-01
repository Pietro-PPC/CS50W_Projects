from markdown2 import markdown
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django import forms
from . import util

import random

""" Search form in sidebar """
class SearchPageForm(forms.Form):
    page = forms.CharField(label="Search page",
        widget=forms.TextInput(attrs={'placeholder':'Page title here...'}))

""" Form to create new page """
class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content", widget=forms.Textarea)

""" Form to edit page """
class EditPageForm(forms.Form):
    content = forms.CharField(label="Content", widget=forms.Textarea)

def notFound(request):
    """
        Page displaying not found message.
    """
    return render(request, "encyclopedia/notFoundPage.html", {
        "form": SearchPageForm()
    })

def wikiPage(request, page):
    """
        Wiki page that renders the text entries.
    """
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
        Returns pages which have query_page as a substring.
    """
    similar_entries = []
    pages = util.list_entries()

    for p in pages:
        if query_page in p:
            similar_entries.append(p)

    return similar_entries

def searchPage(request):
    """ 
        Searches for the page specified in the form.
        If the method is not POST, page is redirected to index.
    """
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
    """
    Page to edit an existing entry.
    If method is POST, redirects to the corresponding wikipage
    If the page does not exist, redirects to notfound page
    """
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
        return HttpResponseRedirect(reverse("encyclopedia:notfound"))

def newPage(request):
    """
    Page with form to create a new page
    If the method is POST and the page name already exists, the page is 
    re-rendered with an error message
    """
    error = False
    entryForm = NewPageForm()

    if request.method == 'POST':
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            if util.get_entry(title) == None:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("encyclopedia:wikipage", args=[title]))
            else:
                error = True
                entryForm = NewPageForm(initial={"title": title, "content": content})
    
    return render(request, "encyclopedia/createPage.html", {
        "form": SearchPageForm(),
        "newpageform": entryForm,
        "error": error
    })

def randomPage(request):
    """
    Redirects to a random existing page
    """
    pages = util.list_entries()
    random.seed()
    page = pages[random.randrange(len(pages))]
    return HttpResponseRedirect(reverse("encyclopedia:wikipage", args=[page]))

def index(request):
    """
    Renders index page
    """
    return render(request, "encyclopedia/index.html", {
        "form": SearchPageForm(),
        "entries": util.list_entries()
    })
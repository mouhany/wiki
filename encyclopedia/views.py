from django.shortcuts import render, redirect
from random import choice

import markdown2
import re

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    try:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": markdown2.markdown(util.get_entry(title))
        })
    except:
        return render(request, "encyclopedia/error.html", {
            "message": "The page you requested was not found."
        })


def search(request):
    title = request.GET['q']
    # Found
    try:
        entry = markdown2.markdown(util.get_entry(title))
        return redirect("entry", title=title)
    # Not found
    except:
        # Create a list that will show suggestion page(s) for search query (if any)
        recommendations = []
        entries = util.list_entries()
        for entry in entries:
            match = re.findall(title, entry, re.IGNORECASE)
            if match:
                recommendations.append(entry)
        return render(request, "encyclopedia/search.html", {
            "title": title,
            "recommendations": recommendations
        })


def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html")
    else:
        title = request.POST['title']
        # Return error if title already exists
        if util.get_entry(title):
            return render(request, "encyclopedia/error.html", {
                "message": "The page you want to create already exists."
            })
        entry = request.POST['entry']
        util.save_entry(title, entry)
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })


def edit(request, title):
    # When user click "Edit" on the entry page
    if request.method == "GET":
        entry = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "entry": entry
        })
    # When user clicked "Save Changes" on the edit page
    else:
        edited_title = request.POST['title']
        edited_entry = request.POST['entry']
        util.save_entry(edited_title, edited_entry)
        return redirect("entry", title=edited_title)


def random(request):
    title = choice(util.list_entries())
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": markdown2.markdown(util.get_entry(title))
    })
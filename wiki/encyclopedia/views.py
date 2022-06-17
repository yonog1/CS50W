import re

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def content(request, entry):
    markdowner = markdown.Markdown()
    entry_page = util.get_entry(entry)
    if entry_page is None:
        return render(request, "encyclopedia/error.html", {
            "entry": entry
        })
    else:
        return render(request, "encyclopedia/content.html", {
            "entry_page": markdowner.convert(entry_page),
            "entry": entry.capitalize()
    })


def error(request, entry):
    return render(request, "encyclopedia/error.html", {
        "entry": entry.capitalize()
    })

def search(request):
    value = request.GET.get('q', '')
    if (util.get_entry(value) is not None):
        return HttpResponseRedirect(reverse("entry_page", kwargs={'entry':value}))
    else:
        substring_entries = []
        for entry in util.list_entries():
            if value.upper() in entry.upper():
                substring_entries.append(entry)

        return render(request, "encyclopedia/index.html", {
            "entries": substring_entries,
            "search": True,
            "value": value
        })

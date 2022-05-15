from audioop import reverse
import re
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
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
        return error(request, entry)
    return render(request, "encyclopedia/content.html", {
        "entry": entry.capitalize(),
        "entry_page": markdowner.convert(entry_page)
    })


def error(request, entry):
    return render(request, "encyclopedia/error.html", {
        "entry": entry.capitalize()
    })

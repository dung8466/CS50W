from django.shortcuts import render
from markdown2 import Markdown
from . import util
from random import choice

def convert_to_html(title):
    content = util.get_entry(title)
    if content is None:
        return None
    else:
        return Markdown().convert(content)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    html_content = convert_to_html(title)
    if html_content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "This entry does not exist"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })

def entry_search(request):
    entry_list = util.list_entries()
    search = request.POST['q']
    if search in entry_list:
        html_content = convert_to_html(search)
        return render(request, "encyclopedia/entry.html", {
            "title": search,
            "content": html_content
        })
    else:
        recommendation = []
        for i in util.list_entries():
            if search.lower() == i.lower():
                return render(request, "encyclopedia/entry.html", {
                    "title": i,
                    "content": convert_to_html(i)
                })
            elif search.lower() in i.lower():
                recommendation.append(i)
        return render(request, "encyclopedia/search.html", {
            "recommendation": recommendation
        })

def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        for i in util.list_entries():
            if title.lower() == i.lower():
                return render(request, "encyclopedia/error.html", {
                    "message": "Page already exists"
                    })
            else:
                util.save_entry(title, content)
                html_content = convert_to_html(title)
                return render(request, "encyclopedia/entry.html", {
                    "title": title,
                    "content": html_content
                    })

def edit(request):
    if request.method == "POST":
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
            })

def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_content = convert_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
            })

def rand(request):
    all_entries = util.list_entries()
    random_entry = choice(all_entries)
    html_content = convert_to_html(random_entry)
    return render(request, "encyclopedia/entry.html", {
        "title": random_entry,
        "content": html_content
        })

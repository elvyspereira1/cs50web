from django.shortcuts import render, redirect
from django import forms
from django.http import JsonResponse

from . import util
import markdown
import random


class NewPageForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={
        'class': 'form-control', 'id': 'id_content', 'style': "display: none"
        }))


class EditPageForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={
        'class': 'form-control', 'id': 'id_content', 'style': "display: none"
        }))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki_entry(request, title):
    entry_content = util.get_entry(title.lower())
    if entry_content is None:
        return render(request, 'encyclopedia/error.html', {'message': f"The page '{title}' does not exist."})
    html_content = markdown.markdown(entry_content)
    title_page = "Wiki | " + title
    return render(request, 'encyclopedia/entry.html', {'title': title, 'title_page': title_page, 'content': html_content})


def search(request):
    query = request.GET.get('q', '').strip()
    if query:
        entries = util.list_search()
        matching_entries = [entry for entry in entries if query.lower() in entry.lower()]
        if len(matching_entries) == 1 and query.lower() == matching_entries[0].lower():
            return redirect('wiki_entry', title=matching_entries[0])
        return render(request, "encyclopedia/search_results.html", {
            "query": query,
            "entries": matching_entries
        })
    return render(request, "encyclopedia/search_results.html", {
        "query": query,
        "entries": []
    })


def new_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title):
                return render(request, "encyclopedia/new_page.html", {
                    "form": form,
                    "error": "An entry with this title already exists."
                })
            else:
                util.save_entry(title, content)
                return redirect('wiki_entry', title=title)
    else:
        form = NewPageForm()
        entries = util.list_entries_clear()
        
    return render(request, "encyclopedia/new_page.html", {
        "form": form,
        "entries": entries
    })


def edit_page(request, title):
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            new_title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content, title_new=new_title)
            return redirect('wiki_entry', title=new_title)
    else:
        content = util.get_entry(title)
        if content is None:
            return render(request, "encyclopedia/error.html", {
                "message": "The requested page was not found."
            })

        lines = content.split('\n', 1)
        if len(lines) > 1 and lines[0].startswith('# '):
            initial_title = lines[0][2:].strip()
            initial_content = lines[1].strip()
        else:
            initial_title = title
            initial_content = content.strip()
        
        form = EditPageForm(initial={'title': initial_title, 'content': initial_content})
        entries = util.list_entries_clear()
    
    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "form": form,
        "entries": entries
    })


def random_page(request):
    entries = util.list_entries_clear()
    if entries:
        random_entry = random.choice(entries)
        return redirect('wiki_entry', title=random_entry)
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "No entries available."
        })
    

def get_entries(request):
    query = request.GET.get('term', '')
    entries = util.list_entries_clear()
    filtered_entries = [entry for entry in entries if query.lower() in entry.lower()]
    return JsonResponse(filtered_entries, safe=False)
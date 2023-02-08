from django.shortcuts import render
import markdown2
from . import util
import random
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse


class NewTaskForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Title', 'style': 'width: 300px; border-radius: 10px;', 'class': 'form-control'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Content', 'style': 'border-radius: 10px; margin-top: 10px; margin-bottom: 10px;', 'class': 'form-control'}))
    
class EditTaskForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Content', 'style': 'border-radius: 10px; margin-top: 10px; margin-bottom: 10px;', 'class': 'form-control'}))

#return the home page
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#return a page that display the content of the entry in the parameter
def entry(request, title):
    return render(request, "encyclopedia/entry.html",{
        "title": title,
        "entry": markdown2.markdown(f"{util.get_entry(title)}"),
        "exist":(util.get_entry(title)) is not None
    })

#return the content of the entry if matched, else return a list of entry that have character's matching the query
def search(request):
    input_value = request.GET.get('q')
    entry_value = util.get_entry(input_value)
    if entry_value is None:
        return render(request, "encyclopedia/search.html", {
            "entries": (util.list_entries()),
            "input": input_value
        })
    return entry(request, input_value)

#create a new entry
def new_entry(request):
    #title_value = request.POST.post('q')
    #content_value = request.POST.post('content')
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if not util.get_entry(title):
                util.save_entry(title, content)
                return entry(request, title)
            else:
                return render(request, "encyclopedia/new.html", {
                "form": form,
                "title": title,
                "entries": util.list_entries(),
                "exist": True
            })
                
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form,
                "exist": False
            })
    return render(request, "encyclopedia/new.html", {
        "form": NewTaskForm(),
        "exist": False
    })
    
#edit entry
def edit_entry(request, title):
    data = {"content": util.get_entry(title)}
    if request.method == "POST":
        form = EditTaskForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content) 
            return entry(request, title)   
        else:
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "form": EditTaskForm(initial=data),
            })
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form": EditTaskForm(initial=data),
    })
    
#return a random encyclopedia entry
def random_entry(request):
    entry_name = random.choice(util.list_entries())
    return entry(request, entry_name)

        

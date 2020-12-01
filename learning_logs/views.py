from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404


# Create your views here.

#when a URL request matches the pattern we just defined,
# Django looks for a function called index() in the views.py file.

def index(request):
    return render(request, 'learning_logs/index.html')


# to get all topics
@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    #A context is a dictionary in which the keys are names we'll use
    # in the template to access the data, and the values are the data
    # we need to send to the template. In this case, there's one key-value pair,
    # which contains the set of topics we'll display on the page. 
    context = {'topics':topics}
    #When building a page that uses data, we pass the context variable to render()
    # as well as the request object and the path to the template

    return render(request, 'learning_logs/topics.html', context)

# get individual topic
@login_required
def topic(request,t_id):
    #just like we did in MyShell.py
    topic = Topic.objects.get(id=t_id)
    # foreign key can be accessed using '_set'
    
    # Make sure the topic belongs to the current user
    if topic.owner != request.user:
        raise Http404


    entries = topic.entry_set.order_by('-date_added') # this makes date_added-' show in descending order

    context = {'topic':topic, 'entries':entries}

    return render(request, 'learning_logs/topic.html', context)

    # Get request - 
    # Post request - 

@login_required
def new_topic(request):
    if request.method != 'POST':
        # No data submitted; create a blank form (create an instance of TopicForm).
        # Because we included no arguments when instantiating TopicForm, Django 
        # creates a blank form that the user can fill out. 
        form = TopicForm()
    else:
        # POST data submitted; process data.
        # We make an instance of TopicForm and pass it the data entered by the user,
        # stored in request.POST.
        form = TopicForm(data=request.POST) # how all the info user gives is on the form 
        # The is_valid() method checks that all required fields have been filled
        # in (all fields in a form are required by default) and that the data entered 
        # matches the field types expected
        if form.is_valid():
            #write the data from the form to the database
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            #return the user's browser to the topics page
            return redirect('learning_logs:topics')
    # Display a blank form using the new_topic.html template        
    context = {'form':form}

    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request,topic_id):
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)

        if form.is_valid():
            # When we call save(), we include the argument commitFalse to tell Django to create
            # a new entry object and assign it to new_entry wihtout saving it to the database yet.
            new_entry = form.save(commit=False)
            # assign the topic of the new entry based on the topic we pulled form topic_id
            new_entry.topic = topic
            new_entry.save()
            form.save()
            return redirect('learning_logs:topic', t_id=topic_id)

    context = {'form': form, 'topic': topic}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid(): 
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry':entry, 'topic':topic, 'form':form}
    return render(request, 'learning_logs/edit_entry.html', context) # context is a dictionary. It has all the data that passes to the HMTL file. 


from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm


# Create your views here.

def index(request):
    return render(request, 'learning_logs/index.html')


# to get all topics
def topics(request):
    topics = Topic.objects.order_by('date_added')
    context = {'topics':topics}

    return render(request, 'learning_logs/topics.html', context)

# get individual topic
def topic(request,t_id):
    topic = Topic.objects.get(id=t_id)
    entries = topic.entry_set.order_by('-date_added') # the '-' makes it shpw in descending order

    context = {'topic':topic, 'entries':entries}

    return render(request, 'learning_logs/topic.html', context)

    # Get request - 
    # Post request - 

def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST) # how all the info user gives is on the form 
        
        if form.is_valid():
            form.save()

            return redirect('learning_logs:topics')
    context = {'form':form}

    return render(request, 'learning_logs/new_topic.html', context)

def new_entry(request,topic_id):
    topic = Topic.objects.get(id=topic_id)
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

def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid(): 
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry':entry, 'topic':topic, 'form':form}
    return render(request, 'learning_logs/edit_entry.html', context) # context is a dictionary. It has all the data that passes to the HMTL file. 


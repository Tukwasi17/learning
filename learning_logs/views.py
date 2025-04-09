from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.urls import reverse
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    """The home page for learning log"""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """show all topic"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {
        'topics': topics
    }
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Show a single topic and all its entries"""
    topic = get_object_or_404(Topic, id=topic_id)
    if topic.owner != request.user:
        raise Http404('You do not have permission to view this topic')
    entries = topic.entries.order_by('-date_added')
    context = {
        'topic': topic,
        'entries': entries
    }
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Add a new topic"""
    if request.method != 'POST':
        # no data submitted, create a blank form
        form = TopicForm()
    else:
        # Post data submitted, process data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect(reverse('learning_logs:topics'))
    context = {
        'form': form
    }    
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Add a new entry for a particular topic"""
    topic = get_object_or_404(Topic, id=topic_id)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect(reverse('learning_logs:topic', args=[topic_id]))
    context = {
        'topic': topic,
        'form': form
    }
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry"""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    #restrict users from editing other users, (if authenticated)
    if request.user != topic.owner:
        return HttpResponseForbidden("You are not allowed to edit this entry")
    
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('learning_logs:topic', args=[topic.id]))

    context = {
        'entry': entry,
        'topic': topic,
        'form': form
    }        
    return render(request, 'learning_logs/edit_entry.html', context)
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound

from notes.models import Notes
from account.models import Account
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from notes.forms import CreateNoteForm, UpdateNoteForm
from blog.models import BlogPost

def get_notes_queryset(id,userrname,query=None):
    print(Notes.share_view)

    queryset = []
    queries = query.split(" ")
    for q in queries:
        notes = Notes.objects.filter(author=id
        ).filter(
            Q(title__icontains=q) |
            Q(body__icontains=q)
        ).distinct()

        for note in notes:
            queryset.append(note)



    for q in queries:
        notes = Notes.objects.all().filter(
            Q(title__icontains=q) |
            Q(body__icontains=q)
        ).distinct()

        for note in notes:
            list_share_view = str(note.share_view).split(',')
            if userrname in list_share_view:
                queryset.append(note)
    for q in queries:
        notes = Notes.objects.all().filter(
            Q(title__icontains=q) |
            Q(body__icontains=q)
        ).distinct()

        for note in notes:
            list_share_view = str(note.share_edit).split(',')
            if userrname in list_share_view:
                queryset.append(note)

    return list(set(queryset))


def create_note_view(request):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')

    form = CreateNoteForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        author = Account.objects.filter(email=user.email).first()
        obj.author = author
        obj.save()
        form = CreateNoteForm()
        return HttpResponseRedirect("/notes")


    context['form'] = form

    return render(request, "notes/create_note.html", context)


def edit_note_view(request, id):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect("must_authenticate")

    notes = get_object_or_404(Notes, pk=id)

    if notes.author != user and user.username not in str(notes.share_edit).split(','):
        return HttpResponse("You are not the author of that post.")

    if request.POST:
        form = UpdateNoteForm(request.POST or None, request.FILES or None, instance=notes)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = "Updated"
            blog_post = obj


    form = UpdateNoteForm(
        initial={
            "title": notes.title,
            "body": notes.body,
            "share_view": notes.share_view,
            "share_edit": notes.share_edit,
        }
    )

    context['form'] = form
    return render(request, 'notes/edit_note.html', context)


def delete_detail_note(request, id):
    user = request.user
    try:
        instance = Notes.objects.get(id=id)

        if instance.author != user:
            return HttpResponse("You are not the author of that note.")

        instance.delete()
        return HttpResponseRedirect("/notes")

    except instance.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")

NOTES_PER_PAGE = 3


def notes_screen_view(request):
    user = request.user
    if user.is_authenticated:
        context = {}


        query = ""
        query = request.GET.get('q', '')
        context['query'] = str(query)


        notes = sorted(get_notes_queryset(request.user.id,request.user.username ,query,), key=attrgetter('date_updated'), reverse=True)


        # Pagination
        page = request.GET.get('page', 1)
        notes_paginator = Paginator(notes ,NOTES_PER_PAGE)

        try:
            notes = notes_paginator.page(page)
        except PageNotAnInteger:
            notes = notes_paginator.page(NOTES_PER_PAGE)
        except EmptyPage:
            notes = notes_paginator.page(NOTES_PER_PAGE.num_pages)

        context['notes'] = notes


        return render(request, "notes/home.html", context)
    else:
        return redirect("login")

def detail_note_view(request, id):
    print(request.user.username)

    context = {}

    user = request.user
    if not user.is_authenticated:
            return redirect("login")
    notes = get_object_or_404(Notes, pk=id)


    if (notes.author != user and user.username not in (str(notes.share_view).split(',') and str(notes.share_edit).split(',')) ):
        return HttpResponse("You are not the author of that note.")

    context['notes'] = notes

    return render(request, 'notes/detail_note.html', context)

def publish(request, id):
    context = {}

    user = request.user
    if not user.is_authenticated:
            return redirect("login")
    notes = get_object_or_404(Notes, pk=id)


    if notes.author != user:
        return HttpResponse("You are not the author of that post.")
    blog_post = BlogPost()
    blog_post.title = notes.title
    blog_post.body = notes.body
    blog_post.author = request.user
    blog_post.save()
    return redirect("/")

def delete_from_share_view(request, id):
    user = request.user
    try:
        instance = Notes.objects.get(id=id)
        list = str(instance.share_view).split(',')
        if user.username in list:
            list.remove(user.username)
            changed_view = ','.join(list)
            instance.share_view = changed_view
            instance.save()

        instance = Notes.objects.get(id=id)
        list = str(instance.share_edit).split(',')
        if user.username in list:
            list=str(instance.share_edit).split(',')
            list.remove(user.username)
            changed_view = ','.join(list)
            instance.share_edit = changed_view
            instance.save()
        return HttpResponseRedirect("/notes")

    except instance.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")
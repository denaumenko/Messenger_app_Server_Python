from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound

from blog.models import BlogPost
from blog.forms import CreateBlogPostForm, UpdateBlogPostForm

from account.models import Account
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator



def create_blog_view(request):

	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate')

	form = CreateBlogPostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		author = Account.objects.filter(email=user.email).first()
		obj.author = author
		obj.save()
		form = CreateBlogPostForm()
		return HttpResponseRedirect("/")

	context['form'] = form

	return render(request, "blog/create_blog.html", context)


def detail_blog_view(request, id):

	context = {}
	user = request.user
	if user.is_authenticated:
		blog_post = get_object_or_404(BlogPost, pk=id)
		context['blog_post'] = blog_post

		return render(request, 'blog/detail_blog.html', context)
	else:
		return redirect("login")


def edit_blog_view(request, id):

	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect("must_authenticate")

	blog_post = get_object_or_404(BlogPost, pk=id)

	if blog_post.author != user:
		return HttpResponse("You are not the author of that post.")

	if request.POST:
		form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=blog_post)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			context['success_message'] = "Updated"
			blog_post = obj

	form = UpdateBlogPostForm(
			initial = {
					"title": blog_post.title,
					"body": blog_post.body,
			}
		)

	context['form'] = form
	return render(request, 'blog/edit_blog.html', context)


def get_blog_queryset(query=None):
	queryset = []
	queries = query.split(" ") # python install 2019 = [python, install, 2019]
	for q in queries:
		posts = BlogPost.objects.filter(
				Q(title__icontains=q) | 
				Q(body__icontains=q)
			).distinct()

		for post in posts:
			queryset.append(post)

	return list(set(queryset))

def delete_detail_blog(request, id):
	try:
		instance = BlogPost.objects.get(id=id)
		instance.delete()
		return HttpResponseRedirect("/")
	except instance.DoesNotExist:
		return HttpResponseNotFound("<h2>Person not found</h2>")


BLOG_POSTS_PER_PAGE = 3


def home_screen_view(request):
	user = request.user
	if user.is_authenticated:

		context = {}

		query = ""
		query = request.GET.get('q', '')
		context['query'] = str(query)

		blog_posts = sorted(get_blog_queryset(query), key=attrgetter('date_updated'), reverse=True)

		# Pagination
		page = request.GET.get('page', 1)
		blog_posts_paginator = Paginator(blog_posts, BLOG_POSTS_PER_PAGE)

		try:
			blog_posts = blog_posts_paginator.page(page)
		except PageNotAnInteger:
			blog_posts = blog_posts_paginator.page(BLOG_POSTS_PER_PAGE)
		except EmptyPage:
			blog_posts = blog_posts_paginator.page(blog_posts_paginator.num_pages)

		context['blog_posts'] = blog_posts


		return render(request, "blog/home.html", context)
	else:
		return redirect("login")
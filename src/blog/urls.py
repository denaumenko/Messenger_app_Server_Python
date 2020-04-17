from django.urls import path
from blog.views import(

	create_blog_view,
	detail_blog_view,
	edit_blog_view,
	delete_detail_blog

)

app_name = 'blog'

urlpatterns = [
	path('create/', create_blog_view, name="create"),
	path('<id>/', detail_blog_view, name="detail"),
	path('<id>/edit', edit_blog_view, name="edit"),
	path('<id>/delete', delete_detail_blog, name="delete"),
]
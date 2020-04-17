from rest_framework import serializers
from blog.models import BlogPost

import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
IMAGE_SIZE_MAX_BYTES = 1024 * 1024 * 2 # 2MB
MIN_TITLE_LENGTH = 5
MIN_BODY_LENGTH = 50




class BlogPostSerializer(serializers.ModelSerializer):

	username = serializers.SerializerMethodField('get_username_from_author')


	class Meta:
		model = BlogPost
		fields = ['pk', 'title', 'slug', 'body', 'date_updated', 'username']


	def get_username_from_author(self, blog_post):
		username = blog_post.author.username
		return username

class BlogPostUpdateSerializer(serializers.ModelSerializer):

	class Meta:
		model = BlogPost
		fields = ['title', 'body']

	def validate(self, blog_post):
		try:
			title = blog_post['title']
			if len(title) < MIN_TITLE_LENGTH:
				raise serializers.ValidationError({"response": "Enter a title longer than " + str(MIN_TITLE_LENGTH) + " characters."})
			
			body = blog_post['body']
			if len(body) < MIN_BODY_LENGTH:
				raise serializers.ValidationError({"response": "Enter a body longer than " + str(MIN_BODY_LENGTH) + " characters."})


		except KeyError:
			pass
		return blog_post


class BlogPostCreateSerializer(serializers.ModelSerializer):


	class Meta:
		model = BlogPost
		fields = ['title', 'body', 'date_updated', 'author']


	def save(self):
		
		try:

			title = self.validated_data['title']
			if len(title) < MIN_TITLE_LENGTH:
				raise serializers.ValidationError({"response": "Enter a title longer than " + str(MIN_TITLE_LENGTH) + " characters."})
			
			body = self.validated_data['body']
			if len(body) < MIN_BODY_LENGTH:
				raise serializers.ValidationError({"response": "Enter a body longer than " + str(MIN_BODY_LENGTH) + " characters."})
			
			blog_post = BlogPost(
								author=self.validated_data['author'],
								title=title,
								body=body,
								)
			blog_post.save()
			return blog_post
		except KeyError:
			raise serializers.ValidationError({"response": "You must have a title, some content."})
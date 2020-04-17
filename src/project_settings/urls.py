from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

from blog.views import (
    home_screen_view,
)
from notes.views import (
    notes_screen_view
)

from account.views import (
    registration_view,
    logout_view,
    login_view,
    account_view,
    must_authenticate_view,
)

from notes.views import (
    detail_note_view,
    create_note_view,
    edit_note_view,
    delete_detail_note,
    publish,
    delete_from_share_view,
)

urlpatterns = [
    path('', home_screen_view, name="home"),
    path('notes/', notes_screen_view, name="notes"),
    path('notes/create/', create_note_view, name="note_create"),
    path('notes/<id>/', detail_note_view, name="detail_note"),
    path('notes/<id>/edit', edit_note_view, name="edit_note"),
    path('notes/<id>/delete', delete_detail_note, name="delete_note"),
    path('notes/<id>/publish',publish, name="publish"),
    path('notes/<id>/delshare',delete_from_share_view, name="delshare"),

    # path('notes/', include('notes.urls', 'notes')),
    path('admin/', admin.site.urls),
    path('account/', account_view, name="account"),
    path('accounts/profile/', home_screen_view, name="home_redirect"),
    path('blog/', include('blog.urls', 'blog')),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('must_authenticate/', must_authenticate_view, name="must_authenticate"),
    path('register/', registration_view, name="register"),
    path('api/v1/',include('social_django.urls', namespace='social')),
    path('api/blog/', include('blog.api.urls', 'blog_api')),  # REST-framework
    path('api/account/', include('account.api.urls', 'account_api')),  # REST-framework
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
         name='password_change_done'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),
         name='password_change'),
    path('password_reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.views import (LoginView,LogoutView,
                                    PasswordResetView,PasswordResetDoneView,
                                    PasswordResetConfirmView,PasswordResetCompleteView)
from django.conf.urls.static import static
from users import views as user_views 
from . import settings



urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',user_views.register,name='register'),
    path('login/',LoginView.as_view(template_name = 'users/login.html'),name='login'),
    path('logout/',LogoutView.as_view(template_name = 'users/logout.html'),name='logout'),
    path('profile/',user_views.profile,name='profile'),
    path('password-reset/',
         PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='password_reset'),
    path('password-reset-done/',
         PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>',
         PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    path('',include('tasks.urls')),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

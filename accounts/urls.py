from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import upload, approve_1, details, status, admin2, details2, director, details3, update, history1, history2, history3

urlpatterns = [
    path('register/', views.registerPage, name = "register"),
    path('login/', views.loginPage, name="login"), 
    path('logout', views.logoutUser, name = "logout"),
    path('', views.home, name = 'home'),
    #path('upload/', upload.as_view()),
    path('upload/', views.upload, name = "upload"),
    path('form_submitted', views.form_submitted, name = "form_submitted"),
    path('approve_1/', approve_1.as_view(), name = "admin1"),
    path('history1/', history1.as_view(), name = "history1"),
    path('admin2/', admin2.as_view(), name = "admin2"),
    path('history2/', history2.as_view(), name = "history2"),
    path('director/', director.as_view(), name = "director"),
    path('history3/', history3.as_view(), name = "history3"),
    #path('details/<int:id>/',views.details, name = 'new'),
    path('details/<int:pk>/', details.as_view(), name = 'new'),
    path('details2/<int:pk>/', details2.as_view(), name = 'new2'),
    path('details3/<int:pk>/', details3.as_view(), name = 'new3'),
    path('info/', views.info, name = 'info'),
    path('status/', views.status, name = 'status'),
    #path('update/<int:pk>/', update.as_view(), name='update'),
    path('update/<int:pk>/', views.update, name = 'update'),

    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), 
        name="password_reset_complete"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

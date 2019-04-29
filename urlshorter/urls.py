from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include, reverse_lazy

from engine.forms import LoginForm, RegisterForm
from engine.views import *

accounts_urls = [
    path(
        'login/',
        LoginView.as_view(template_name="login.html", authentication_form=LoginForm),
        name='login'
    ),
    path(
        'register/',
        CreateView.as_view(
            template_name='register.html',
            model=User,
            form_class=RegisterForm,
            success_url=reverse_lazy('main')
        ),
        name='register'
    ),
    path(
        'logout/',
        LogoutView.as_view(template_name="logout.html"),
        name='logout'
    ),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="main.html"), name='main'),
    path('shorten/', ShortUrlView.as_view(), name='short_url'),
    path('links/', UserLinksView.as_view(), name='user_links_list'),
    path('link/<str:url>', UserLinkDetailView.as_view(), name='user_link_detail'),
    path('accounts/', include(accounts_urls)),
    path('<str:url>', RedirectUrlView.as_view()),
]

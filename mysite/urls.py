"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from . import views

admin.autodiscover()

urlpatterns = [
    url(r'^$', views.index),
    url(r'^admin/', admin.site.urls),

    #bets
    url(r'^bets/$', views.bets),
    url(r'^bet/(\d{1,5})', views.bet_detail),
    url(r'^bets/add$', views.add_bet_form),

    #comments
    url(r'^comments/remove/(\d{1,5})/(\d{1,5})', views.remove_comment),


    #accounts
    url(r'^accounts/', include('allauth.urls')),
    url(r'logout/', views.logout_view),

    #friends
    url(r'^friend/(\d{1,5})', views.friend_detail),
    url(r'^add/(\d{1,5})', views.add_friend),

]

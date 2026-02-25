from django.urls import path, include
from . import views
from .views import ShopAPIView

urlpatterns = [
    path('', views.index, name='home'),

    path('basket', views.basket, name='basket'),
    path('register/', views.Register.as_view(), name='register'),
    path('api/v1/shoplist/', ShopAPIView.as_view()),
    path('', include('django.contrib.auth.urls')),
    path('email_confirm/', views.email_confirm, name='email_confirm'),
    path('add_to_menu/', views.add_to_menu, name='add_to_menu'),
    path('profil/', views.profil, name='profil'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('game/', views.game, name='game'),
    path('search1/', views.search1, name='search1'),

]

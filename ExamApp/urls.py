from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('wishes', views.home),
    path('logout', views.logout),
    path('wishes/new',views.addWish),
    path('wishes/<int:id>/delete', views.deleteWish),
    path('wishes/<int:id>/edit',views.edit),
    path('wishes/<int:id>/edit1',views.editWish),
    path('wishes/<id>/grant',views.grantwish),

]



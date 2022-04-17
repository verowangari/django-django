from django.urls import path,include
from .import views
from django.contrib.auth import views as authViews
from App.views import Signup
urlpatterns=[
    path('',views.index,name='index'),
    path('login/', authViews.LoginView.as_view(template_name='login.html'), name='login'),
    path('signup/', Signup, name='signup'),
    path('logout/', authViews.LogoutView.as_view(), {'next_page' : 'index'}, name='logout'),
    path('newpost/', views.NewPost, name='newpost'),
    path('newhood/', views.CreateHood, name='newhood'),
    path('allhoods/', views.hoods, name='allhoods'),
    path('join_hood/<id>', views.join_hood, name='join-hood'),
    path('leave_hood/<id>', views.leave_hood, name='leave-hood'),
    path('singlehood/<hood_id>', views.SingleHood, name='singlehood'),
]

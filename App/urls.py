from django.urls import path,include
from .import views
from django.contrib.auth import views as authViews
from App.views import Signup
urlpatterns=[
    path('',views.index,name='index'),
    path('login/', authViews.LoginView.as_view(template_name='login.html'), name='login'),
    path('signup/', Signup, name='signup'),
    path('logout/', authViews.LogoutView.as_view(), {'next_page' : 'index'}, name='logout'),
]

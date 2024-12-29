from django.urls import path
from .views import Tlist, Tdetail, Tcreate, Tupdate, Tdelete, Userlogin, Userregister
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', Userlogin.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view(next_page='login'), name = 'logout'),
    path('register/', Userregister.as_view(), name = 'register'),
    path('', Tlist.as_view(), name = 'alltask'),
    path('todolist/<int:pk>/', Tdetail.as_view(), name = 'todolist'),
    path('create/', Tcreate.as_view(), name = 'create'),
    path('update/<int:pk>/', Tupdate.as_view(), name = 'update'),
    path('delete/<int:pk>/', Tdelete.as_view(), name = 'delete'),
]
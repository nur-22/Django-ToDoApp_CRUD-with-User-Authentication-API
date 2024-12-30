from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from .models import Todolist
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# API
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import TodolistSerializer

# User login
class Userlogin(LoginView):
    template_name = 'todolist/login.html'  # customized template name

    def get_success_url(self):
        return reverse_lazy('alltask')  # to generate the URL

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('alltask')
        return super().dispatch(request, *args, **kwargs)

# User registration
class Userregister(FormView):
    template_name = 'todolist/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('alltask')

    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('alltask')
        return super().dispatch(request, *args, **kwargs)

# List of all tasks
class Tlist(LoginRequiredMixin, ListView):
    model = Todolist
    context_object_name = 'alltask'

    def get_queryset(self):
        return Todolist.objects.filter(user=self.request.user)

# Task details
class Tdetail(LoginRequiredMixin, DetailView):
    model = Todolist
    context_object_name = 'singletask'

# Add a new task
class Tcreate(LoginRequiredMixin, CreateView):
    model = Todolist
    fields = ['task', 'description', 'completed']
    success_url = reverse_lazy('alltask')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# Edit a task
class Tupdate(LoginRequiredMixin, UpdateView):
    model = Todolist
    fields = ['task', 'description', 'completed']
    success_url = reverse_lazy('alltask')

# Delete a task
class Tdelete(LoginRequiredMixin, DeleteView):
    model = Todolist
    context_object_name = 'singletask'
    success_url = reverse_lazy('alltask')

# API ViewSet
class TodolistViewSet(viewsets.ModelViewSet):
    serializer_class = TodolistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Todolist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

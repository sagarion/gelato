from django.shortcuts import render

from django.shortcuts import render
from client.models import Client
from django.views.generic import ListView, DetailView


class UserListView(ListView):
    queryset = Client.objects.select_related()

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        return context
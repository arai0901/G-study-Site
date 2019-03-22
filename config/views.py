from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from item.models import Shou, Prob, Shintyoku
from django.urls import reverse
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin

class index(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return redirect(reverse('item:top_page'))

index = index.as_view()

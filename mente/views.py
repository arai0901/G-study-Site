from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from item.models import Shou, Prob, Shintyoku
from django.urls import reverse, reverse_lazy
from mente.forms import ProbForm, ShouForm
from django.views.generic import UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

class Shou_Registration(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = ShouForm()
        context = {'form':form}

        return render(request, 'mente/shou_registration.html', context=context)

    def post(self, request, *args, **kwargs):
        form = ShouForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('item:top_page'))
        else:
            return render(request, 'mente/shou_registration.html', {'form':form})

shou_registration = Shou_Registration.as_view()

class Pre_Registration(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        form_ = Shou.objects.all()
        form = []
        for i in range(len(form_)):
            form__ = [i+1, form_[i].shou_name, form_[i].id]
            form.append(form__)
        print(form)
        context = {'form':form}

        return render(request, 'mente/pre_registration.html', context=context)

pre_registration = Pre_Registration.as_view()


class Registration(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        shou_id = int(kwargs['shou_id'])

        try:
            last_num = Prob.objects.filter(shou_id=shou_id).order_by('-prob_num')[0].prob_num
        except:
            last_num = 0

        form = ProbForm(initial={"shou_id":Shou.objects.get(id=shou_id).id, "prob_num":last_num+1})
        context = {'form':form, 'shou_id':shou_id}
        return render(request, 'mente/registration.html', context=context)

    def post(self, request, *args, **kwargs):
        shou_id = int(kwargs['shou_id'])
        form = ProbForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse('mente:pre_registration'))
        else:
            return render(request, 'mente/registration.html', {'form':form})



registration = Registration.as_view()


class Pre_edit(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        probs = Prob.objects.all().order_by('prob_num').order_by('shou_id')

        shou_num = probs

        forms = []
        for prob in probs:
            froms.append( [ prob, int((prob.shou_id - 2)/10) ] )

        context = {'form':form}

        return render(request, 'mente/pre_edit.html', context=context)

pre_edit = Pre_edit.as_view()

class Edit(LoginRequiredMixin, UpdateView):
    model = Prob
    form_class = ProbForm
    template_name = 'mente/edit.html'
    success_url = reverse_lazy('mente:pre_edit')

class Pre_delete(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        probs = Prob.objects.all().order_by('prob_num').order_by('shou_id')
        context = {'probs':probs}

        return render(request, 'mente/pre_delete.html', context=context)

pre_delete = Pre_delete.as_view()


class Delete(LoginRequiredMixin, DeleteView):
    model = Prob
    form_class = ProbForm
    template_name = 'mente/delete.html'
    success_url = reverse_lazy('mente:pre_delete')

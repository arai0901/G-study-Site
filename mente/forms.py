from django import forms
from item.models import Prob, Shou

class ProbForm(forms.ModelForm):
    class Meta:
        model = Prob
        fields = '__all__'

class ShouForm(forms.ModelForm):
    class Meta:
        model = Shou
        fields = '__all__'

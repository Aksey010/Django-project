from django import forms


class ResultsForm(forms.Form):
    vacancy = forms.CharField(label='Вакансия')
    city = forms.CharField(label='Город')

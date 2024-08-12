from django.shortcuts import render, HttpResponseRedirect
from .models import Search, Requirements, Skill
from .forms import ResultsForm
from django.urls import reverse, reverse_lazy
from modules.parsing_modul import hh_parser
from django.views.generic import ListView, FormView, TemplateView
# Create your views here.


class IndexListView(ListView):
    model = Search
    template_name = 'hh_parser/index.html'
    paginate_by = 2


# Не смог придумать, как использовать cbv, так как не нашёл способ достать значения из формы и использовать из в url
# class FormListView(FormView):
#
#     form_class = ResultsForm
#
#     template_name = 'hh_parser/form.html'
#
#     success_url = reverse_lazy('parser:results', kwargs={'vacancy': 'Юрист', 'city': 'Москва'})
    # def get_success_url(self, **kwargs):
    #     return reverse_lazy('parser:results', kwargs={'vacancy': self.kwargs['vacancy'], 'city': self.kwargs['city']})


def form(request):
    if request.method == 'POST':
        form = ResultsForm(request.POST)
        if form.is_valid():
            vacancy = form.cleaned_data['vacancy']
            city = form.cleaned_data['city']

            return HttpResponseRedirect(reverse('parser:results', kwargs={'vacancy': vacancy, 'city': city}))
        else:
            return render(request, 'hh_parser/form.html', context={'form': form})
    else:
        form = ResultsForm()
        return render(request, 'hh_parser/form.html', context={'form': form})


class ContactsTemplateView(TemplateView):
    template_name = 'hh_parser/contacts.html'


# Не смог придумать, как использовать cbv
def results(request, vacancy, city):
    try:
        obj = Search.objects.get(vacancy=vacancy, city=city)
        skills = []
        world_id = obj.id
        for d in Requirements.objects.filter(world_id=world_id).values():
            # print(d, '*'*60)
            id_s = d['skill_id']
            skills.append(Skill.objects.filter(id=id_s).values()[0]['name'])

        if not skills:
            skills = 'Нет информации'
    except:
        data = hh_parser(vacancy, city)
        # print(data)
        obj = data[0]
        skills = data[1]

    return render(request, 'hh_parser/results.html', context={'obj': obj, 'skills': skills})

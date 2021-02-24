from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Menu, Category
from django.views import generic
from .forms import LocationRegisterForm


class MenuList(generic.ListView):
    model = Category

class MenuDetail(generic.DetailView):
    model = Menu

def location_register(request):
    form = LocationRegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        request.session['location'] = request.POST['location'][0]
        return redirect('ec:menu_list')

    context = {
        'form': form
    }
    return render(request, 'ec/location_register.html', context)

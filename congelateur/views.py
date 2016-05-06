from django.shortcuts import render, render_to_response, get_object_or_404
from congelateur.models import Glace, Congelateur, Categorie
from django.views.generic import TemplateView, ListView, DetailView

# Create your views here.


def accueil(request):
    return render(request, 'congelateur/accueil.html', locals())

def about(request):
    return render(request, 'congelateur/about.html')

def discover(request):
    return render(request, 'congelateur/discover.html', locals())

def dashboard(request):
    return render(request, 'congelateur/dashboard.html', locals())

def home(request):
    return render(request, 'congelateur/home.html')



class GlaceView(TemplateView):
    template_name = 'congelateur/glace_list.html'

    def get_context_data(self, **kwargs):
        context = super(GlaceView, self).get_context_data(**kwargs)
        context['glaces'] = Glace.objects.all()
        context['cats'] = Categorie.objects.all()
        return context


def lire(request, p_id):
    categorie = get_object_or_404(Categorie, id=p_id)
    glaces = []

    if categorie.sousCategorie is None:

        lesCat = Categorie.objects.filter(sousCategorie=categorie.id)

        for p in lesCat:
            pk = p.id
            uneCat = Glace.objects.filter(cat=pk)
            for u in uneCat:
                glaces.append(u)
    else:
        glaces = Glace.objects.filter(cat=p_id)

    toutesLesCats = Categorie.objects.all()

    return render(request, 'congelateur/glace_categorie.html', {'cat': categorie, 'gl': glaces, 'cats':toutesLesCats})


class CongelateurListView(ListView):
    queryset = Congelateur.objects.select_related()

    def get_context_data(self, **kwargs):
        context = super(CongelateurListView, self).get_context_data(**kwargs)
        return context

class CongelateurDetailView(DetailView):
    model = Congelateur
    def get_context_data(self, **kwargs):
        context = super(CongelateurDetailView, self).get_context_data(**kwargs)
        return context



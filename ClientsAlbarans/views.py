from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, FormView

from ClientsAlbarans.form import ClientForm, AlbaraForm, EditarClientForm, BuscarAlbaraForm, \
    EditarEstatAlbaraForm, AfegirLineaAlbaraForm, RegisterForm, LoginForm, MarcarPreparacioForm, ReposicioForm
from ClientsAlbarans.models import Client, Albara, Producte, Categoria, LineaAlbara, StockMagatzem, Magatzem


# Create your views here.

class PaginaPrincipal(TemplateView):
    template_name = 'ClientsAlbarans/inici.html'

# - - - LLISTAR OBJECTES - - -
class LlistaClients(ListView):
    model = Client
    template_name = 'ClientsAlbarans/llista_clients.html'
    context_object_name = 'clients'

class LlistaAlbarans(LoginRequiredMixin,ListView):
    model = Albara
    template_name = 'ClientsAlbarans/llista_albarans.html'
    context_object_name = 'albarans'

# - - - CREAR OBJECTES - - -

class CrearClient(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'ClientsAlbarans/formulari.html'
    success_url = reverse_lazy('ClientsAlbarans:inici')
    extra_context = {'title': 'Crear Client'}

class CrearAlbara(LoginRequiredMixin,CreateView):
    model = Albara
    form_class = AlbaraForm
    template_name = 'ClientsAlbarans/formulari.html'
    success_url = reverse_lazy('ClientsAlbarans:inici')
    extra_context = {'title': 'Crear Albara'}

# - - - DETAILLS - - -

class DetailsClient(DetailView):
    model = Client
    template_name = 'ClientsAlbarans/detalls_clients.html'
    extra_context = {'title': 'Details Client'}

class DetailsAlbara(LoginRequiredMixin,DetailView):
    model = Albara
    template_name = 'ClientsAlbarans/detalls_albara.html'
    extra_context = {'title': 'Details Albara'}

# - - - EDICIÓ - - -

class EditarClient(UpdateView):
    model = Client
    form_class = EditarClientForm
    template_name = 'ClientsAlbarans/formulari.html'
    success_url = reverse_lazy('ClientsAlbarans:clients')
    extra_context = {'title': 'Editar Client'}


class EditarEstatAlbara(LoginRequiredMixin,UpdateView):
    model = Albara
    form_class = EditarEstatAlbaraForm
    template_name = 'ClientsAlbarans/formulari.html'
    success_url = reverse_lazy('ClientsAlbarans:albarans')
    extra_context = {'title': 'Editar estat Albara'}

class Cataleg(ListView):
    model = Categoria
    template_name = 'ClientsAlbarans/cataleg.html'
    context_object_name = 'cataleg'

    def get_queryset(self):
        # Prefetch productos activos y guardarlos en 'productes_actius'
        return Categoria.objects.prefetch_related(
            Prefetch(
                'categories_productes',  # relación normal Django
                queryset=Producte.objects.filter(actiu=True),
                to_attr='productes_actius'  # aqui guardamos el resultado
            )
        )

class ProducteCategoria(ListView):
    model = Producte
    template_name = 'ClientsAlbarans/FiltrarCategoria.html'
    context_object_name = 'productes'
    extra_context = {'title': 'Categoria amb els seus productes'}

    def get_queryset(self):
        return Producte.objects.filter(categoria_id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categoria'] = Categoria.objects.get(pk=self.kwargs['pk'])
        return context

class Consulta(LoginRequiredMixin,FormView):
    model = Albara
    form_class = BuscarAlbaraForm
    template_name = 'ClientsAlbarans/Buscador.html'
    context_object_name = 'albarans'
    extra_context = {'title': 'Buscar Albara'}

    def form_valid(self, form):
        numero = form.cleaned_data['numero_albara']
        return redirect('ClientsAlbarans:consultaResultat', pk=numero)

class ConsultaResultat(LoginRequiredMixin,DetailView):
    model = Albara
    template_name = 'ClientsAlbarans/ConsultaResultat.html'
    context_object_name = 'albara'
    extra_context = {'title': 'Consulta Resultat'}

    def get_object(self, queryset=None):
        numero_albara = self.kwargs['pk']
        return Albara.objects.get(pk=numero_albara)

class AfegirLineaAlbara(LoginRequiredMixin,CreateView):
    model = LineaAlbara
    form_class = AfegirLineaAlbaraForm
    template_name = 'ClientsAlbarans/formulari.html'
    extra_context = {'title': 'Afegir Linea Albara'}
    success_url = reverse_lazy('ClientsAlbarans:inici')

    def form_valid(self, form):
        albara = get_object_or_404(Albara, pk=self.kwargs['pk'])
        linea = form.save(commit=False)
        linea.albara = albara
        linea.save()
        return super().form_valid(form)


class Preparacio(LoginRequiredMixin,ListView):
    model = Albara
    template_name = 'ClientsAlbarans/preparacioAlbarans.html'
    extra_context = {'title': 'Albarans en preparació'}
    context_object_name = 'albarans'

    def get_queryset(self):
   #     empleat = self.request.user.empleat
   #     magatzem = empleat.magatzem_assignat
        return Albara.objects.filter(estat__in=['EN_PREPARACIO', 'PENDENT'])


class MarcarPreparacio(LoginRequiredMixin,UpdateView):
    model = Albara
    template_name = 'ClientsAlbarans/formulari.html'
    extra_context = {'title': 'Marcar preparacio'}
    form_class = MarcarPreparacioForm
    success_url = reverse_lazy('ClientsAlbarans:inici')


class StockView(LoginRequiredMixin,ListView):
    model = StockMagatzem
    template_name = 'ClientsAlbarans/stocklist.html'
    context_object_name = 'stocks'

    def get_queryset(self):
        qs = StockMagatzem.objects.select_related('producte','magatzem','producte__categoria')

        magatzem_id = self.request.GET.get('magatzem')
        categoria_id = self.request.GET.get('categoria')

        if magatzem_id:
            qs = qs.filter(magatzem=magatzem_id)

        if categoria_id:
            qs = qs.filter(producte__categoria_id=categoria_id)

            return qs.order_by('producte__nom')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['magatzems'] = Magatzem.objects.all()
        context['categories'] = Categoria.objects.all()
        return context

class StockReposicio(LoginRequiredMixin,FormView):
    form_class = ReposicioForm
    template_name = 'ClientsAlbarans/stock_reposicio.html'
    extra_context = {'title': 'Stock Reposicio'}
    success_url = reverse_lazy('ClientsAlbarans:inici')

    def form_valid(self, form):
        magatzem = form.cleaned_data['magatzem']
        producte = form.cleaned_data['producte']
        quantitat = form.cleaned_data['quantitat']

        quantitat = int(quantitat)

        stock, created = StockMagatzem.objects.get_or_create(
            magatzem=magatzem,
            producte=producte,
            defaults={'quantitat': quantitat,
                      'data_ultima_entrada': timezone.now(),}
        )
        if not created:
            # Actualizamos cantidad y fecha de la última entrada
            stock.quantitat = int(stock.quantitat) + quantitat
            stock.data_ultima_entrada = timezone.now()
            stock.save()

        return super().form_valid(form)

class Register(FormView):
    form_class = RegisterForm
    template_name = 'ClientsAlbarans/register.html'
    success_url = reverse_lazy('ClientsAlbarans:inici')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class Login(FormView):
    form_class = LoginForm
    template_name = 'ClientsAlbarans/login.html'

    def form_valid(self, form):
        user = form.cleaned_data.get('user')
        if not user:
            return self.form_invalid(form)

        login(self.request, user)
        return redirect('ClientsAlbarans:inici')








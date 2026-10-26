import django.contrib.auth
from django.contrib.auth.views import LoginView
from django.urls import path
from django.contrib.auth import views as auth_views
from ClientsAlbarans.views import PaginaPrincipal, LlistaClients, CrearClient, CrearAlbara, \
    DetailsClient, EditarClient, DetailsAlbara, Cataleg, ProducteCategoria, Consulta, ConsultaResultat, \
    EditarEstatAlbara, AfegirLineaAlbara, LlistaAlbarans, Preparacio, Register, Login, MarcarPreparacio, StockView, \
    StockReposicio

app_name = 'ClientsAlbarans'

urlpatterns = [
    path('', PaginaPrincipal.as_view(), name='inici'),

    # - - - LLISTAR DADES - - -
    path('clients/', LlistaClients.as_view(), name='clients'),
    path('albarans/', LlistaAlbarans.as_view(), name='albarans'),

    # - - - CREAR DADES - - -
    path('client/nou', CrearClient.as_view(), name='crear_client'),

    path('albara/nou', CrearAlbara.as_view(), name='crear_albara'),
    path('albara/<int:pk>/estat', EditarEstatAlbara.as_view(), name='editar_estat_albara'),
    path('albara/<int:pk>/afegir-linea', AfegirLineaAlbara.as_view(), name='afegir_linea_albara'),

    path('cataleg/', Cataleg.as_view(), name='cataleg'),
    path('cataleg/<int:pk>/', ProducteCategoria.as_view(), name='ProducteCategoria'),

    path('clients/<int:pk>/',DetailsClient.as_view(), name='detalls_client'),
    path('albarans/<int:pk>/', DetailsAlbara.as_view(), name='detalls_albara'),
    path('clients/<int:pk>/editar', EditarClient.as_view(), name='editar_client'),

    path('consulta/', Consulta.as_view(), name='consulta'),
    path('consulta/<int:pk>/', ConsultaResultat.as_view(), name='consultaResultat'),

    path('preparacio/', Preparacio.as_view(), name='preparacio'),
    path('preparacio/<int:pk>/', MarcarPreparacio.as_view(), name='marcar_preparacio'),

    path('stock/',StockView.as_view(), name='stock'),

    path('stock/reposicio/', StockReposicio.as_view(), name='stock_reposicioy com'),

    path('register/', Register.as_view(), name='registre'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')


    ]
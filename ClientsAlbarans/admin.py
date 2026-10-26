from django.contrib import admin

from ClientsAlbarans.models import Client, Albara, LineaAlbara, Producte, Categoria, Magatzem, StockMagatzem, Empleat

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Producte)
admin.site.register(Magatzem)
admin.site.register(Empleat)
admin.site.register(StockMagatzem)
admin.site.register(Client)
admin.site.register(Albara)
admin.site.register(LineaAlbara)
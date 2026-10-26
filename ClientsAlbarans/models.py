from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Categoria(models.Model):
    nom = models.CharField(max_length=100)
    descripcio = models.CharField(max_length=100)
    requereix_refrigeracio = models.BooleanField(default=False)
    temperatura_maxima = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.nom

    class Meta:
        ordering = ['nom']
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categories'

class Producte(models.Model):
    UNITAT_MESURA = [
        ("UNITAT", "Unitat"),
        ("CAIXA", "Caixa"),
        ("PALET", "Enviat"),
        ("KG", "Kg"),
        ("LITRE", "Litre"),
    ]

    codi = models.CharField(unique=True,max_length=100)
    nom = models.CharField(max_length=100)
    descripcio = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='categories_productes')
    preu_unitari = models.CharField(max_length=100)
    unitat =  models.CharField(max_length=100,choices=UNITAT_MESURA)
    iva = models.DecimalField(decimal_places=2, max_digits=10)
    es_perible = models.BooleanField(default=False)
    imatge_url = models.CharField(max_length=100)
    actiu = models.BooleanField(default=False)


    def __str__(self):
        return self.nom

    class Meta:
        ordering = ['nom']
        verbose_name = 'Producte'
        verbose_name_plural = 'Productes'

class Magatzem(models.Model):
    nom = models.CharField(max_length=100)
    adreca = models.CharField(max_length=100)
    capacitat_maxima = models.CharField(max_length=100)
    te_cambra_fret = models.BooleanField(default=False)
    responsable = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ['nom']
        verbose_name = 'Magatzem'
        verbose_name_plural = 'Magatzems'


class StockMagatzem(models.Model):

     producte = models.ForeignKey(Producte, on_delete=models.CASCADE, related_name='stock_productes')
     magatzem = models.ForeignKey(Magatzem, on_delete=models.CASCADE, related_name='magatzems')
     quantitat = models.CharField(max_length=100)
     data_ultima_entrada = models.DateField()
     ubicacio = models.CharField(max_length=100)

     def __str__(self):
         return str(self.magatzem)

     class Meta:
         ordering = ['quantitat']
         verbose_name = 'StockMagatzem'
         verbose_name_plural = 'StockMagatzems'


class Client(models.Model):
    codi_client = models.CharField(unique=True,max_length=100)
    nom_comercial = models.CharField(max_length=100)
    cif = models.CharField(max_length=20)
    persona_contacte =models.CharField(max_length=100)
    telefon =models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    adreca_entrega = models.CharField(max_length=100)
    poblacion = models.CharField(max_length=100)
    codi_postal = models.CharField(max_length=100)
    actiu = models.BooleanField(default=True)

    def __str__(self):
        return self.codi_client

    class Meta:
        ordering = ['codi_client']
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

class Empleat(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='empleat')
    codi_empleat = models.CharField(unique=True,max_length=100)
    telefon =models.CharField(max_length=20)
    data_alta = models.DateField()
    magatzem_assignat = models.ForeignKey('Magatzem', on_delete=models.CASCADE, related_name='magatzems_assignats', null=True, blank=True)
    carrec = models.CharField(max_length=100)

    def __str__(self):
        return self.codi_empleat

    class Meta:
        ordering = ['codi_empleat']
        verbose_name = 'Empleat'
        verbose_name_plural = 'Empleats'


class Albara(models.Model):
    TIPUS_ESTAT = [
        ('PENDENT', 'Pendent'),
        ('EN_PREPARACIO', 'Preparacio'),
        ('ENVIAT', 'Enviat'),
        ('ENTREGAT', 'Entregat'),
        ('CANCELAT', 'Cancelat')

    ]
    numero_albara = models.CharField(unique=True,max_length=100)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='clients_albara')
    empleat = models.ForeignKey(Empleat, on_delete=models.CASCADE, related_name='clients_empleat')
    magatzem = models.ForeignKey(Magatzem, on_delete=models.CASCADE, related_name='magatzems_albara')
    data_creacio = models.DateTimeField(auto_now_add=True)
    data_entrega_prevista = models.DateField()
    estat = models.CharField(choices=TIPUS_ESTAT,max_length=100)
    base_imposable = models.DecimalField(decimal_places=2, max_digits=10)
    iva_total = models.DecimalField(decimal_places=2, max_digits=10)
    total = models.DecimalField(decimal_places=2, max_digits=10)
    observacions = models.CharField(null=True, blank=True,max_length=200)
    signatura_client = models.CharField(null=True, blank=True,max_length=100)

    def __str__(self):
        return self.numero_albara

    class Meta:
        ordering = ['numero_albara']
        verbose_name = 'Albara'
        verbose_name_plural = 'Albarans'

        # -------------------------------
        # Método para recalcular totales
        # -------------------------------
    def recalcular_totales(self):
        self.base_imposable = sum(linea.subtotal for linea in self.albaran.all())
        self.iva_total = self.base_imposable * Decimal('0.21')
        self.total = self.base_imposable + self.iva_total
        self.save(update_fields=['base_imposable', 'iva_total', 'total'])


class LineaAlbara(models.Model):

    albara = models.ForeignKey(Albara, on_delete=models.CASCADE, related_name='albaran')
    producte = models.ForeignKey(Producte, on_delete=models.CASCADE, related_name='productes_albara')
    quantitat = models.IntegerField()
    preu_unitari = models.DecimalField(max_digits=10, decimal_places=2)
    descompte_percentatge = models.CharField(max_length=3)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.CharField(null=True, blank=True,max_length=200)


    def __str__(self):
        return str(self.albara)


    class Meta:
        ordering = ['albara']
        verbose_name = 'Linea Albara'
        verbose_name_plural = 'Lineas Albarans'

    def save(self, *args, **kwargs):
        # Calculamos el subtotal automáticamente
        desc = Decimal(self.descompte_percentatge or 0) / Decimal('100')
        self.subtotal = self.quantitat * self.preu_unitari * (Decimal('1') - desc)

        super().save(*args, **kwargs)

        self.albara.recalcular_totales()



from django.contrib import admin
from django import forms
from gamerauntsia.txapelketak.models import Txapelketa, Partida, Partaidea
from forms import PartidaInlineForm, TxapelketaAdminForm
from mptt.admin import MPTTModelAdmin

class PartidaForm(forms.ModelForm): 
    def __init__(self, *args, **kwargs):
        super(PartidaForm, self).__init__(*args, **kwargs)
        wtf = Partaidea.objects.filter(txapelketa=self.instance.txapelketa_id);
        w = self.fields['partaideak'].widget
        choices = []
        for choice in wtf:
            choices.append((choice.id, choice.get_izena()))
        w.choices = choices


class PartidaAdmin(MPTTModelAdmin):

    def get_partaideak(self, obj):
        return " VS ".join([p.get_izena() for p in obj.partaideak.all()])

    list_display = ('txapelketa', 'jardunaldia','get_partaideak','emaitza', 'average', 'date')
    filter_horizontal = ('partaideak',)
    raw_id_fields = ('parent','txapelketa')
    search_fields = ['txapelketa__izena']
    list_filter = ('txapelketa',)
    ordering = ('-date',)
    form = PartidaForm
    
    fieldsets = (
        ('Datu orokorrak',
        {'fields':('jardunaldia','txapelketa')},),
        ('Konfigurazioa',
        {'fields':('partaideak','parent','is_return','date')},),
        ('Emaitza',
        {'fields':('emaitza','average')},),
        ('Bideoa',
        {'fields':('bideoa','start','end')},),
    )



class PartidaInline(admin.TabularInline):
    model = Partida
    fields = ('jardunaldia','partaideak','emaitza','parent','date')
    form = PartidaInlineForm

class TxapelketaAdmin(admin.ModelAdmin):

    def preview(self,obj):
        return '<a href="/txapelketak/%s">%s</a>' % (obj.slug, obj.slug)
    preview.allow_tags=True

    list_display = ('izena', 'preview','mota', 'modalitatea','jokoa','insk_date','pub_date', 'status', 'publikoa_da')
    prepopulated_fields = {"slug": ("izena",)}
    filter_horizontal = ('jokalariak','adminak')
    raw_id_fields = ('irudia','jokoa')
    list_filter = ('mota','modalitatea', 'publikoa_da')
    search_fields = ['izena','slug']
    ordering = ('-pub_date',)
    form = TxapelketaAdminForm
    #inlines = [PartidaInline]

class PartaideakForm(forms.ModelForm): 
    def __init__(self, *args, **kwargs):
        super(PartaideakForm, self).__init__(*args, **kwargs)
        wtf = []
        if Txapelketa.objects.filter(id=self.instance.txapelketa_id).exists():
            wtf = Txapelketa.objects.get(id=self.instance.txapelketa_id).get_jokalariak()
        w = self.fields['jokalariak'].widget
        choices = []
        for choice in wtf:
            choices.append((choice.id, choice.getFullName()))
        w.choices = choices

class PartaideakAdmin(admin.ModelAdmin):

    def get_izena(self, obj):
        if not obj.izena:
            if len(obj.jokalariak.all()) == 1:
                return obj.jokalariak.all()[0].username
            else:
                return ", ".join([p.username for p in obj.jokalariak.all()])
        return obj.izena

    list_display = ('txapelketa', 'get_izena', 'win','lose', 'matches','points')
    filter_horizontal = ('jokalariak',)
    raw_id_fields = ('irudia','txapelketa')
    search_fields = ['izena']
    ordering = ('-id',)
    form = PartaideakForm
    
    fieldsets = (
        ('Datu orokorrak',
        {'fields':('izena','irudia','txapelketa')},),
        ('Jokalariak',
        {'fields':('kapitaina','jokalariak')},),
        ('Puntuazioa',
        {'fields':('win','lose','draw','matches','average','points')},),
        ('Txapelketaren irabazlea',
        {'fields':('irabazlea',)},),
    )

admin.site.register(Txapelketa,TxapelketaAdmin)
admin.site.register(Partida,PartidaAdmin)
admin.site.register(Partaidea,PartaideakAdmin)

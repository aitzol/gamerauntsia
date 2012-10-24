from tutorialak.models import Tutoriala, Gaia
from aplikazioak.models import Aplikazioa
from base.models import Base
from berriak.models import Berria
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    h = {}
    h['aplikazioak'] = Aplikazioa.objects.all()
    h['gaiak'] = Gaia.objects.all()
    h['berriak'] = Berria.objects.filter(publikoa_da=True).order_by('-pub_date')[:5]
    return render_to_response('tutorialak/index.html', h,context_instance=RequestContext(request))
    
def tutoriala(request,slug):
    h = {}
    h['item'] = Tutoriala.objects.filter(slug=slug)[0]
    h['berriak'] = Berria.objects.filter(publikoa_da=True).order_by('-pub_date')[:5]
    return render_to_response('tutorialak/tutoriala.html', h,context_instance=RequestContext(request))
    
def gaiak(request):
    h = {}
    h['gaiak'] = Gaia.objects.all()
    h['berriak'] = Berria.objects.filter(publikoa_da=True).order_by('-pub_date')[:5]
    return render_to_response('tutorialak/gaiak.html', h,context_instance=RequestContext(request))
    
def gaia(request,slug):
    h = {}
    h['zerr_tutoriala'] = Tutoriala.objects.filter(gaia__slug=slug, publikoa_da=True).order_by('-pub_date')[:10]
    h['gaia'] = Gaia.objects.filter(slug=slug)[0]
    h['berriak'] = Berria.objects.filter(publikoa_da=True).order_by('-pub_date')[:5]
    return render_to_response('tutorialak/gaia.html', h,context_instance=RequestContext(request))
    
def tutorialak_aplikazioa(request,aplikazioa):
    h = {}
    tutorial_list = Tutoriala.objects.filter(aplikazioa__izena=aplikazioa).order_by('-pub_date')
    paginator = Paginator(tutorial_list, 6)
    page = request.GET.get('orria')
    try:
        tutorialak = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tutorialak = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        tutorialak = paginator.page(paginator.num_pages)
    h['tutorialak'] = tutorialak
    h['aplikazioa'] = Aplikazioa.objects.get(izena=aplikazioa)
    h['berriak'] = Berria.objects.filter(publikoa_da=True).order_by('-pub_date')[:5]
    return render_to_response('tutorialak/tutorialak_aplikazioa.html', h,context_instance=RequestContext(request))
    
def tutorialak_gaia(request,gaia):
    h = {}
    tutorial_list = Tutoriala.objects.filter(gaia__izena=gaia).order_by('-pub_date')
    paginator = Paginator(tutorial_list, 6)
    page = request.GET.get('orria')
    try:
        tutorialak = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tutorialak = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        tutorialak = paginator.page(paginator.num_pages)
    h['tutorialak'] = tutorialak
    h['gaia'] = Gaia.objects.get(izena=gaia)
    h['zerr_tutoriala'] = Tutoriala.objects.filter(publikoa_da=True).order_by('-pub_date')[:10]
    h['berriak'] = Berria.objects.filter(publikoa_da=True).order_by('-pub_date')[:5]
    return render_to_response('tutorialak/tutorialak_gaia.html', h,context_instance=RequestContext(request))   
    
    
def bozkatuenak(request):
    h = {}
    tutorial_list = Tutoriala.objects.filter(publikoa_da=True).order_by('-puntuak','-botoak')
    paginator = Paginator(tutorial_list, 8) # Show 25 contacts per page
    page = request.GET.get('orria')
    try:
        tutorialak = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tutorialak = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        tutorialak = paginator.page(paginator.num_pages)
    h['base'] = Base.objects.all()[0]
    h['tutorialak'] = tutorialak
    h['berriak'] = Berria.objects.filter(publikoa_da=True).order_by('-pub_date')[:5]
    return render_to_response('base/index.html', h,context_instance=RequestContext(request))
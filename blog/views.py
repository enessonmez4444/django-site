import io, json, csv, base64, requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from google import genai

# Modeller ve Formlar
from .models import (
    Ders, Dokuman, Video, Uygulama, VeriSeti, 
    DersTamamlama, AltBaslik, AltBaslikTamamlama, Alistirma
)
from .forms import ContactForm

# Makine Öğrenmesi
from sklearn.linear_model import LinearRegression, LogisticRegression, Lasso
from sklearn.preprocessing import PolynomialFeatures
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.naive_bayes import GaussianNB

# --- AYARLAR ---
GEMINI_API_KEY = "AIzaSyC852bn8hRYjOO1_tx_LUzZ2uxiLtCsvHo"
client = genai.Client(api_key=GEMINI_API_KEY)
YOUTUBE_URL = "https://www.youtube.com/@pythontürkçeakademi"

# --- ANA SAYFA ---
def ana_sayfa(request):
    # YouTube URL'sini her ihtimale karşı context ile gönderiyoruz
    return render(request, 'blog/ana_sayfa.html', {'youtube_url': YOUTUBE_URL})

# --- DERS SİSTEMİ ---
def ders_detay(request, slug):
    ders = get_object_or_404(Ders, slug=slug)
    alt_basliklar = ders.alt_basliklar.all().prefetch_related('alistirmalar').order_by('sira')
    tum_dersler = Ders.objects.filter(parent__isnull=True).prefetch_related('alt_basliklar').order_by('sira')

    if request.user.is_authenticated:
        tamamlanan = AltBaslikTamamlama.objects.filter(
            kullanici=request.user,
            alt_baslik__in=alt_basliklar,
            tamamlandi=True
        ).values_list('alt_baslik_id', flat=True)
    else:
        tamamlanan = []

    onceki_ders = Ders.objects.filter(sira__lt=ders.sira, parent__isnull=True).order_by('-sira').first()
    sonraki_ders = Ders.objects.filter(sira__gt=ders.sira, parent__isnull=True).order_by('sira').first()

    context = {
        'ders': ders,
        'alt_basliklar': alt_basliklar,
        'tamamlanan_alt_basliklar': list(tamamlanan),
        'tum_dersler': tum_dersler,
        'onceki_ders': onceki_ders,
        'sonraki_ders': sonraki_ders,
        'youtube_url': YOUTUBE_URL
    }
    return render(request, 'blog/ders_detay.html', context)

def python_dersleri(request):
    ilk_ders = Ders.objects.all().order_by('sira').first()
    if ilk_ders:
        return redirect('ders_detay', slug=ilk_ders.slug)
    return render(request, 'blog/python_dersleri.html')

# --- ÜYELİK ---
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, "Başarıyla kayıt oldunuz!")
            return redirect('ana_sayfa')
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

# --- DİĞER SAYFALAR ---
def uygulamalar_view(request):
    uygulamalar = Uygulama.objects.all().order_by('sira')
    return render(request, 'blog/uygulamalar.html', {'uygulamalar': uygulamalar})

def videolar(request):
    videolar_list = Video.objects.all().order_by('sira')
    return render(request, 'blog/videolar.html', {'videolar': videolar_list})

def kod_kutuphanesi(request): return render(request, 'blog/kod_kutuphanesi.html')
def projeler(request): return render(request, 'blog/projeler.html')
def blog_page(request): return render(request, 'blog/blog.html')
def hakkimda(request): return render(request, 'blog/hakkimda.html')

def dokumanlar(request): 
    docs = Dokuman.objects.all()
    return render(request, 'blog/dokumanlar.html', {'dokumanlar': docs})

# --- İLETİŞİM ---
def iletisim(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Mesajınız gönderildi!")
            return redirect('iletisim')
    else:
        form = ContactForm()
    return render(request, 'blog/iletisim.html', {'form': form})

# --- AI ASİSTAN ---
def ai_asistan(request):
    ai_cevap = None
    if request.method == "POST":
        soru = request.POST.get("soru")
        if soru:
            modeller = ["gemini-2.0-flash", "gemini-1.5-flash"]
            for model_adi in modeller:
                try:
                    response = client.models.generate_content(model=model_adi, contents=soru)
                    if response.text:
                        ai_cevap = response.text
                        break
                except:
                    continue
    return render(request, "blog/ai_chat.html", {"ai_cevap": ai_cevap})

# --- VERİ VE GRAFİK ---
def veri_analizi(request):
    if request.GET.get('temizle'):
        for key in ['yuklenen_veri','veri_kaynagi']:
            request.session.pop(key, None)
        return redirect('veri_analizi')
    
    veri = None
    if 'yuklenen_veri' in request.session:
        veri = pd.read_json(io.StringIO(request.session['yuklenen_veri']), orient='split')
    
    tablo_html = veri.to_html(classes="table table-striped") if veri is not None else None
    return render(request, "blog/veri_analizi.html", {"tablo_html": tablo_html, "veri_var_mi": veri is not None})

plt.switch_backend('Agg')
def grafik_olustur(request):
    grafik_base64 = None
    if request.method == "POST":
        try:
            x = [float(i) for i in request.POST.get("x_deger","").split(",")]
            y = [float(i) for i in request.POST.get("y_deger","").split(",")]
            plt.figure(figsize=(6,4))
            plt.plot(x, y, marker='o')
            buf = io.BytesIO()
            plt.savefig(buf, format="png")
            grafik_base64 = base64.b64encode(buf.read()).decode('utf-8')
            plt.close()
        except: pass
    return render(request, "blog/grafik.html", {"grafik_base64": grafik_base64})

# --- AJAX İŞLEMLERİ ---
@login_required
@require_POST
def alt_baslik_tamamla(request):
    data = json.loads(request.body)
    alt_id = data.get('alt_baslik_id')
    AltBaslikTamamlama.objects.update_or_create(
        kullanici=request.user, alt_baslik_id=alt_id, defaults={'tamamlandi': True}
    )
    return JsonResponse({'success': True})

@csrf_exempt
def alistirma_kontrol(request):
    if request.method == "POST":
        data = json.loads(request.body)
        alistirma = get_object_or_404(Alistirma, id=data.get('id'))
        if alistirma.dogru_cevap.lower() == data.get('cevap', '').strip().lower():
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error'})

# Makine Öğrenimi (Basitleştirilmiş)
def makine_ogrenimi(request):
    return render(request, "blog/makine_ogrenimi.html")

def web_scraping(request):
    return render(request, "blog/web.html")

def scraping_csv(request):
    return HttpResponse("CSV Hazırlanıyor...")
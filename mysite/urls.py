from django.contrib import admin
from django.urls import path, include
from blog import views
from django.contrib.auth import views as auth_views

# --- MEDYA DOSYALARI İÇİN GEREKLİ IMPORTLAR ---
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # --- ADMIN PANEL ---
    path('admin/', admin.site.urls),

    # --- ANA SAYFA ---
    path('', views.ana_sayfa, name='ana_sayfa'),

    # --- GİRİŞ / ÜYELİK SİSTEMİ ---
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='ana_sayfa'), name='logout'),
    path('register/', views.register, name='register'),

    # --- DERS SİSTEMİ ---
    path('dersler/', views.python_dersleri, name='python_dersleri'),
    path('dersler/<slug:slug>/', views.ders_detay, name='ders_detay'),

    # --- AI ASİSTAN ---
    path('ai/', views.ai_asistan, name='ai'),

    # --- VERİ ANALİZİ ---
    path('veri-analizi/', views.veri_analizi, name='veri_analizi'),

    # --- GRAFİK OLUŞTURMA ---
    path('grafik-analizi/', views.grafik_olustur, name='grafik_olustur'),

    # --- UYGULAMALAR VE VİDEOLAR ---
    path('uygulamalar/', views.uygulamalar_view, name='uygulamalar'),
    path('videolar/', views.videolar, name='videolar'),

    # --- KOD KÜTÜPHANESİ VE PROJELER ---
    path('kod-kutuphanesi/', views.kod_kutuphanesi, name='kod_kutuphanesi'),
    path('projeler/', views.projeler, name='projeler'),

    # --- BLOG SAYFASI ---
    path('blog/', views.blog_page, name='blog_page'),

    # --- DOKÜMANLAR VE HAKKIMDA ---
    path('dokumanlar/', views.dokumanlar, name='dokumanlar'),
    path('hakkimda/', views.hakkimda, name='hakkimda'),
    path('makine-ogrenimi/', views.makine_ogrenimi, name='makine_ogrenimi'),

    # --- İLETİŞİM ---
    path('iletisim/', views.iletisim, name='iletisim'),
    path("web-scraping/", views.web_scraping, name="web_scraping"),
    path("scraping-csv/", views.scraping_csv, name="scraping_csv"),
    path('alt_baslik_tamamla/', views.alt_baslik_tamamla, name='alt_baslik_tamamla'),
    path('alistirma-kontrol/', views.alistirma_kontrol, name='alistirma_kontrol'),
]

# --- MEDYA DOSYALARI SERVİS AYARI (BU KISIM EKSİKTİ) ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
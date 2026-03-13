from django.contrib import admin
from django.urls import path
from blog import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.ana_sayfa, name='ana_sayfa'),

    # Giriş / Üyelik
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='ana_sayfa'), name='logout'),
    path('register/', views.register, name='register'),

    # Dersler
    path('dersler/', views.python_dersleri, name='python_dersleri'),
    path('dersler/<slug:slug>/', views.ders_detay, name='ders_detay'),

    # Alt başlık tamamlama (AJAX)
    path('alt_baslik_tamamla/', views.alt_baslik_tamamla, name='alt_baslik_tamamla'),

    # AI
    path('ai/', views.ai_asistan, name='ai'),

    # Diğer sayfalar
    path('veri-analizi/', views.veri_analizi, name='veri_analizi'),
    path('grafik-analizi/', views.grafik_olustur, name='grafik_olustur'),
    path('uygulamalar/', views.uygulamalar_view, name='uygulamalar'),
    path('videolar/', views.videolar, name='videolar'),
    path('kod-kutuphanesi/', views.kod_kutuphanesi, name='kod_kutuphanesi'),
    path('projeler/', views.projeler, name='projeler'),
    path('blog/', views.blog_page, name='blog_page'),
    path('dokumanlar/', views.dokumanlar, name='dokumanlar'),
    path('hakkimda/', views.hakkimda, name='hakkimda'),
    path('makine-ogrenimi/', views.makine_ogrenimi, name='makine_ogrenimi'),
    path('iletisim/', views.iletisim, name='iletisim'),
    path('web-scraping/', views.web_scraping, name='web_scraping'),
    path('scraping-csv/', views.scraping_csv, name='scraping_csv'),
    path('alistirma-kontrol/', views.alistirma_kontrol, name='alistirma_kontrol'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
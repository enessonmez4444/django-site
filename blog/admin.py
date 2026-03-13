from django.contrib import admin
from .models import (
    Ders, ContactMessage, Dokuman, Video, Uygulama, 
    VeriSeti, KullaniciVeri, Alistirma, AltBaslik, AltBaslikTamamlama
)

# -----------------------------
# 1. Alıştırma Satırları (Alt Başlığın içinde görünecek)
# -----------------------------
class AlistirmaInline(admin.TabularInline):
    model = Alistirma
    extra = 1  # Her seferinde en az 1 tane boş satır gösterir
    fields = ('soru_metni', 'kod_taslagi', 'dogru_cevap', 'sira')

# -----------------------------
# 2. Alt Başlık Admin (ASIL BURASI: Hem alt başlık hem alıştırma tek ekranda)
# -----------------------------
@admin.register(AltBaslik)
class AltBaslikAdmin(admin.ModelAdmin):
    # Liste ekranında görünecek sütunlar
    list_display = ('baslik', 'ders', 'sira', 'id')
    # Filtreleme ve Arama
    list_filter = ('ders',)
    search_fields = ('baslik',)
    # Liste ekranında sırayı direkt değiştirebilme
    list_editable = ('sira',)
    # İŞTE SİHİRLİ NOKTA: Alt başlık ekleme sayfasının altına alıştırmaları gömer
    inlines = [AlistirmaInline]

# -----------------------------
# 3. Diğer Modeller (Hepsini koruduk)
# -----------------------------
@admin.register(Ders)
class DersAdmin(admin.ModelAdmin):
    list_display = ('baslik', 'sira', 'parent')
    prepopulated_fields = {'slug': ('baslik',)}
    search_fields = ('baslik',)

@admin.register(Alistirma)
class AlistirmaAdmin(admin.ModelAdmin):
    list_display = ('id', 'alt_baslik', 'dogru_cevap', 'sira')
    list_filter = ('alt_baslik__ders',)

@admin.register(AltBaslikTamamlama)
class AltBaslikTamamlamaAdmin(admin.ModelAdmin):
    list_display = ('kullanici', 'alt_baslik', 'tamamlandi')
    list_filter = ('tamamlandi', 'kullanici')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('isim', 'email', 'konu', 'olusturulma_tarihi')
    search_fields = ('isim', 'email')

@admin.register(Dokuman)
class DokumanAdmin(admin.ModelAdmin):
    list_display = ('baslik', 'olusturma_tarihi')

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('baslik', 'sira')
    list_editable = ('sira',)

@admin.register(Uygulama)
class UygulamaAdmin(admin.ModelAdmin):
    # 'sira' ilk başta olduğu için Django link veremiyor. 
    # 'list_display_links' ile linki 'baslik' alanına atayarak sorunu çözüyoruz.
    list_display = ('sira', 'baslik', 'kategori', 'tarih')
    list_editable = ('sira',)
    list_display_links = ('baslik',) # Linki 'baslik' sütununa verdik, hata çözüldü!
    list_filter = ('kategori', 'tarih')
    search_fields = ('baslik', 'kategori')
    fields = ('baslik', 'kategori', 'aciklama', 'icerik', 'kod', 'sira')

@admin.register(VeriSeti)
class VeriSetiAdmin(admin.ModelAdmin):
    list_display = ('isim', 'olusturan', 'olusturulma_tarihi')

@admin.register(KullaniciVeri)
class KullaniciVeriAdmin(admin.ModelAdmin):
    list_display = ('isim', 'kullanici', 'yuklenme_tarihi')
from django.db import models
from django.contrib.auth.models import User

# -----------------------------
# Ders Modeli
# -----------------------------
class Ders(models.Model):
    baslik = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    icerik = models.TextField(default='')
    sira = models.IntegerField(default=0)
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='alt_dersler',  # eski 'alt_basliklar' çakışmayı önledik
        verbose_name="Üst Başlık (Boş bırakılırsa ana başlıktır)"
    )

    class Meta:
        verbose_name_plural = "Dersler"
        ordering = ['sira']

    def __str__(self):
        if self.parent:
            return f"   ↳ {self.baslik}"
        return self.baslik

# -----------------------------
# Alt Başlık Modeli
# -----------------------------
class AltBaslik(models.Model):
    ders = models.ForeignKey(
        Ders,
        on_delete=models.CASCADE,
        related_name='alt_basliklar'  # artık sadece AltBaslik için geçerli
    )
    baslik = models.CharField(max_length=200)
    icerik = models.TextField(blank=True, default='')
    sira = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Alt Başlıklar"
        ordering = ['sira']

    def __str__(self):
        return f"{self.ders.baslik} → {self.baslik}"

# -----------------------------
# İletişim Mesajları
# -----------------------------
class ContactMessage(models.Model):
    isim = models.CharField(max_length=100)
    email = models.EmailField()
    konu = models.CharField(max_length=150)
    mesaj = models.TextField()
    olusturulma_tarihi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.isim} - {self.konu}"

# -----------------------------
# Dokümanlar
# -----------------------------
class Dokuman(models.Model):
    baslik = models.CharField(max_length=255)
    pdf = models.FileField(upload_to='dokumanlar/')
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.baslik

# -----------------------------
# Video Modeli
# -----------------------------
class Video(models.Model):
    baslik = models.CharField(max_length=200)
    youtube_link = models.URLField()
    aciklama = models.TextField(blank=True)
    sira = models.IntegerField(default=0)

    class Meta:
        ordering = ['sira']

    def __str__(self):
        return self.baslik

# -----------------------------
# Uygulama Modeli
# -----------------------------
class Uygulama(models.Model):
    baslik = models.CharField(max_length=200)
    aciklama = models.TextField()
    kategori = models.CharField(max_length=100, blank=True)
    icerik = models.TextField(blank=True, null=True, verbose_name="Uygulama Çalışma Alanı")
    kod = models.TextField(blank=True, verbose_name="Python Kaynak Kodu")
    sira = models.IntegerField(default=0)
    tarih = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sira']

    def __str__(self):
        return self.baslik

# -----------------------------
# Sistem Veri Setleri
# -----------------------------
class VeriSeti(models.Model):
    isim = models.CharField(max_length=200)
    aciklama = models.TextField(blank=True)
    csv_dosya = models.FileField(upload_to='veri_setleri/', blank=True, null=True)
    olusturan = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    olusturulma_tarihi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.isim

# -----------------------------
# Kullanıcıya Özel Yüklenen Dosyalar
# -----------------------------
class KullaniciVeri(models.Model):
    kullanici = models.ForeignKey(User, on_delete=models.CASCADE)
    isim = models.CharField(max_length=150)
    dosya = models.FileField(upload_to='kullanici_verileri/')
    yuklenme_tarihi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.isim} ({self.kullanici.username})"

# -----------------------------
# Ders Tamamlama
# -----------------------------
class DersTamamlama(models.Model):
    kullanici = models.ForeignKey(User, on_delete=models.CASCADE)
    ders = models.ForeignKey(Ders, on_delete=models.CASCADE)
    tamamlandi = models.BooleanField(default=False)
    tamamlanma_tarihi = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['kullanici', 'ders'], name='unique_kullanici_ders')
        ]
        verbose_name = "Ders Tamamlama"
        verbose_name_plural = "Ders Tamamlamaları"

    def __str__(self):
        durum = "Tamamlandı" if self.tamamlandi else "Tamamlanmadı"
        return f"{self.kullanici.username} - {self.ders.baslik} ({durum})"

# -----------------------------
# Alt Başlık Tamamlama
# -----------------------------
class AltBaslikTamamlama(models.Model):
    kullanici = models.ForeignKey(User, on_delete=models.CASCADE)
    alt_baslik = models.ForeignKey(AltBaslik, on_delete=models.CASCADE)
    tamamlandi = models.BooleanField(default=False)
    tamamlanma_tarihi = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['kullanici', 'alt_baslik'], name='unique_kullanici_alt_baslik')
        ]
        verbose_name = "Alt Başlık Tamamlama"
        verbose_name_plural = "Alt Başlık Tamalamaları"

    def __str__(self):
        durum = "Tamamlandı" if self.tamamlandi else "Tamamlanmadı"
        return f"{self.kullanici.username} - {self.alt_baslik.baslik} ({durum})"



class Alistirma(models.Model):
    alt_baslik = models.ForeignKey('AltBaslik', on_delete=models.CASCADE, related_name='alistirmalar')
    soru_metni = models.TextField(help_text="Örn: Aşağıdaki değişkeni 'meyve' adıyla tanımlayın.")
    kod_taslagi = models.TextField(help_text="Örn: ... = 'Elma'")
    dogru_cevap = models.CharField(max_length=255, help_text="Örn: meyve")
    ipucu = models.CharField(max_length=255, blank=True, null=True)
    sira = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sira']

    def __str__(self):
        return f"{self.alt_baslik.baslik} - Alıştırma {self.id}"
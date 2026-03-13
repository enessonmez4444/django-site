from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Ana Sayfa (Bunu eklemeyi unutma!)
    path('', views.ana_sayfa, name='ana_sayfa'),

    # Kayıt Ol (Senin views.py içindeki fonksiyonun)
    path('register/', views.register, name='register'),

    # Giriş Yap (Django'nun hazır sistemi - template_name belirterek)
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),

    # Çıkış Yap (Django'nun hazır sistemi)
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Diğer sayfaların (Örnekler)
    path('python-dersleri/', views.python_dersleri, name='python_dersleri'),
    path('uygulamalar/', views.uygulamalar, name='uygulamalar'),
]
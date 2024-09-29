from django.urls import path
from django.conf import settings
from .views import home, about, service, pricing, blog, blog_details, contact, catalogue, store, genstores, get_districts, get_stores, search_medicines
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('about', about, name='about'),
    path('service', service, name='service'),
    path('pricing', pricing, name='pricing'),
    path('blog', blog, name='blog'),
    path('blogdetails', blog_details, name='blog_details'),
    path('contact', contact, name='contact'),
    path('catalogue/', catalogue, name='catalogue'),
    path('store', store, name='store'),
    path('genstores', genstores, name='genstores'),
    path('get-districts/', get_districts, name='get_districts'),
    path('get-stores/', get_stores, name='get_stores'),
    path('catalogue-list/', search_medicines, name='catalogue-list'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

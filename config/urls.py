from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from board.sitemaps import ThreadSitemap, CategorySitemap
from base.sitemaps import BaseSitemap

sitemaps = {
    'topic': ThreadSitemap,
    'cateogry': CategorySitemap,
    'base': BaseSitemap,
}
urlpatterns = [
    path('admin/', admin.site.urls),
    path('board/', include("board.urls")),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include('api.urls')),
    path('search/', include('search.urls')),
    path('', include('accounts.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
]

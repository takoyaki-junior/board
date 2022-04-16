from django.contrib.sitemaps import Sitemap
from django.shortcuts import resolve_url

from . models import Thread, Category


class ThreadSitemap(Sitemap):
    priority = 0.5
    changefreq = 'always'

    def items(self):
        return Thread.objects.all()

    def location(self, obj):
        return resolve_url('board:detail', pk=obj.id)


class CategorySitemap(Sitemap):
    priority = 0.5
    changefreq = 'never'

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return resolve_url('board:category', url_code=obj.url_code)

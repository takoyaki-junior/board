from django.contrib.sitemaps import Sitemap
from django.shortcuts import resolve_url


class BaseSitemap(Sitemap):

    def items(self):
        items = [
            'board:index',
            'board:policy',
            'board:terms',
        ]
        return items

    def location(self, obj):
        return resolve_url(obj)

    def changefreq(self, obj):
        if obj == 'board:index':
            return 'always'
        return 'never'

    def priority(self, obj):
        if obj == 'board:index':
            return 0.8
        return 0.1

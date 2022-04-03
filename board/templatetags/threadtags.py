from django.template import Library
from django.db.models import Count
from ..models import Category

register = Library()


@register.inclusion_tag('board/tags/category_tag.html')
def categorytag():
    ctx = {}
    ctx['category_list'] = Category.objects.annotate(
        count=Count('name')).order_by('sort')
    return ctx

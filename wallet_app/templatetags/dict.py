from django import template

register = template.Library()


@register.filter('dict_key')
def dict_key(d, k):
    return d[k]

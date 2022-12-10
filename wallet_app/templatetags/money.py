from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()


@register.filter('currency')
def currency(value):
    return f'R$ {intcomma(value)}' if value else 'R$ 0'


@register.filter('percent')
def percent(value):
    percent_value = value * 100
    return f'{round(percent_value, 2)}%'

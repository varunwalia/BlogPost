from urllib import quote_plus
from django import template

register = template.Library()

@register.filter('urlify')
def urlify(value):
	return quote_plus(value)
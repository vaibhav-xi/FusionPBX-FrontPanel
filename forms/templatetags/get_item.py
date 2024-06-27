from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, '')

@register.simple_tag
def increment_counter(counter):
    return counter + 1
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Dictionary'den güvenli şekilde değer al"""
    if dictionary and key in dictionary:
        return dictionary[key]
    return ''
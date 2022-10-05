from django import template

register = template.Library()


@register.filter('startswith')
def startswith(text, value):
    if isinstance(text, str):
        if text.startswith(value) :
            return 'active'
    return ''

@register.filter('deleteFirstSlash')
def deleteFirstSlash(text):
    if isinstance(text, str):
        text = text[1:]
    return text

@register.filter('isActive')
def isActive(text, value):
    if isinstance(text, str):
        if text == value :
            return 'active'
    return ''

@register.filter('isSelected')
def isSelected(text, value):
    if isinstance(text, str):
        if text == value :
            return 'true'
    return 'false'
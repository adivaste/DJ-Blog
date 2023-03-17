from django import template
from django.utils.html import strip_tags

register = template.Library()

@register.filter
def clean_text(value):
    """
    Replaces &nbsp; with a space and strips all HTML tags from the text.
    Usage: {{ some_text|clean_text }}
    """
    cleaned_text =  strip_tags(value).replace("&nbsp;", " ")
    if len(cleaned_text) > 140 :
        return cleaned_text[1:140] + " ..."
    return cleaned_text

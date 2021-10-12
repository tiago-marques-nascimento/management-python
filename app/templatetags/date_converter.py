from django import template

register = template.Library()

def date_converter(value):
    return value.strftime("%d/%m/%Y")

register.filter('date_converter', date_converter)

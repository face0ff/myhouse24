from django import template

register = template.Library()



@register.filter()
def to_int(value):
    return int(' '.join([char for char in value if char.isdigit()]))+1


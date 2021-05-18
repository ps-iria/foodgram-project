from django import template

register = template.Library()


@register.filter
def hex_to_rgb(value):
    value = value.lstrip('#')
    result = str(tuple(int(value[i:i + 2], 16) for i in (0, 2, 4)))
    result = result[:-1]
    result += ', 0.12)'
    return f'rgba{result}'

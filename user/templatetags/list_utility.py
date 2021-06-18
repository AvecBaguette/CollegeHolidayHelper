from django import template

register = template.Library()


def get_item_by_index(list_param, index):
    return list_param[int(index)]


register.filter(get_item_by_index)

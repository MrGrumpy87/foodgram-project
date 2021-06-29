from urllib.parse import urlencode

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def tag_active(context, tag):
    tags_on = context['request'].GET.getlist('tags', [])
    if not tags_on:
        return 'tags__checkbox_active'
    else:
        if tag in tags_on:
            return 'tags__checkbox_active'
    return ''


@register.simple_tag(takes_context=True)
def tag_href(context, tag):
    tags_get = context['request'].GET.getlist('tags', [])
    index = context['request'].path
    if not tags_get:
        tags_on = [tag.slug for tag in context['tags']]
        tags_on.remove(tag)
    else:
        if tag in tags_get:
            tags_get = list(filter(lambda a: a != tag, tags_get))
        else:
            tags_get.append(tag)
        tags_on = tags_get
    g_filter = urlencode({'tags': tags_on}, doseq=True)
    qs = f'{index}?{g_filter}'
    return qs


@register.filter
def recipes_all(count):
    if count >= 3:
        return count - 3
    return 0

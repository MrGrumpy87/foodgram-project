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
			tags_get.remove(tag)
		else:
			tags_get.append(tag)
		tags_on = tags_get
	g_filter = urlencode({'tags': tags_on}, doseq=True)
	qs = f'{index}?{g_filter}'
	return qs


@register.filter
def recipes_all(count):
	return count - 3

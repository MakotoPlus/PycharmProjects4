from django import template
register = template.Library()

@register.simple_tag
def query_string(request, page_number):
    """GETパラメータを一部を置き換える"""
    querydict = request.GET.copy()
    querydict['page'] = page_number
    return querydict.urlencode()


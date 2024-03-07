from datetime import datetime
from django import template

register = template.Library()

@register.simple_tag
def days_difference_with_current_date(date):
    delta = datetime.now().date() - date
    return delta.days

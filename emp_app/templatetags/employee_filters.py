from django import template

register = template.Library()

@register.filter(name='filter_by_dept')
def filter_by_dept(employees, dept_id):
    # This is a placeholder filter.
    # It doesn't perform any filtering, but it prevents the TemplateSyntaxError.
    return employees

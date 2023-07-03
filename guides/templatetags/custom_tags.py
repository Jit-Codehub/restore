from django import template
from django.template import Template, Context

register = template.Library()


def renderTemplate(content, context):
    template = Template(content)
    context = Context(context)
    content = template.render(context)
    return content


@register.filter(name="render_template_content")
def renderTemplateContent(content, context):
    return renderTemplate(content, context)

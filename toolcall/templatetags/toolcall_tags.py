# -*- coding: utf-8 -*-

from django import template


register = template.Library()


@register.simple_tag
def start_toolcall(tool):
    if not tool.slug:
        return ''
    redirect_url = 'https://afr.norsktest.no/toolcall/end-user-test/tools/'
    icon = '<img src="%s"><br>' % tool.icon if tool.icon else ''
    name = tool.name or tool.slug
    startbtn = """
    <div style="display:inline-flex;flex-direction:column;">
    <button client='{tool.client.name}'
            tool='{tool.slug}'
            onclick='window.open("{starturl}", "{tool.client.name}", "width=1024,height=768,scroll=1,resize=1");return false;' 
            class='btn btn-default'>
        {icon}
        {name}
    </button>
    <small>{tool.description}</small>
    </div>
    """.format(
        tool=tool,
        icon=icon, 
        name=name, 
        starturl=redirect_url + tool.slug + '/'
    )
    return startbtn

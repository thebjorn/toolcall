# -*- coding: utf-8 -*-

"""toolcall admin.
"""
from django.contrib import admin
from .models import Client, Tool, ToolCall, ToolCallLog


class ToolInlineAdmin(admin.TabularInline):
    model = Tool
    fields = """slug name description icon restartable restart_duration_minutes
             """.split()
    extra = 1


class ClientAdmin(admin.ModelAdmin):
    list_display = """id client_secret 
                      receive_start_token_url
                      receive_start_data_url
                      receive_result_token_url
                      """.split()
    inlines = [ToolInlineAdmin]


class ToolCallLogAdmin(admin.TabularInline):
    model = ToolCallLog
    # fields = """timestamp status details""".split()
    fields = """status details""".split()
    extra = 0


class ToolCallAdmin(admin.ModelAdmin):
    list_display = """tool user started ended status""".split()
    inlines = [ToolCallLogAdmin]


admin.site.register(Client, ClientAdmin)
admin.site.register(ToolCall, ToolCallAdmin)

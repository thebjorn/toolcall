# -*- coding: utf-8 -*-

"""toolcall admin.
"""
from django.contrib import admin
from .models import Client, Tool


class ToolInlineAdmin(admin.TabularInline):
    model = Tool
    fields = """slug name description icon
             """.split()
    extra = 1


@admin.site.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = """id client_secret 
                      receive_start_token_url
                      receive_start_data_url
                      receive_result_token_url
                      """.split()
    inlines = [ToolInlineAdmin]



# class ToolcallResultAdmin(admin.ModelAdmin):
#     list_display = """id tstamp persnr toolcall_participant_id exam
#                       score passed
#                    """.split()
#     search_fields = "user__persnr toolcall_participant_id".split()
#     list_filter = ['exam']
#     raw_id_fields = ['user']
#
#     def persnr(self, item):
#         return item.user.persnr
#
#
# admin.site.register(ToolcallResult, ToolcallResultAdmin)

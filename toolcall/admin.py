# -*- coding: utf-8 -*-

"""Toolcall admin.
"""
# from django.contrib import admin
# from toolcall.models import ToolcallResult
#
#
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

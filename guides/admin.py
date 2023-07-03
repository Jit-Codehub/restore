from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.urls import reverse
from django.db import models
from django import forms


class BlogAboutInline(admin.StackedInline):
    formfield_overrides = {
        models.CharField : {"widget" : forms.TextInput(attrs={"size":100})},
        models.URLField : {"widget" : forms.URLInput(attrs={"size":100})},
    }
    model = BlogAbout
    can_delete = True
    extra = 0
    
class BlogMentionInline(admin.StackedInline):
    formfield_overrides = {
        models.CharField : {"widget" : forms.TextInput(attrs={"size":100})},
        models.URLField : {"widget" : forms.URLInput(attrs={"size":100})},
    }
    model = BlogMention
    can_delete = True
    extra = 0

class BlogCitationInline(admin.StackedInline):
    formfield_overrides = {
        models.CharField : {"widget" : forms.TextInput(attrs={"size":100})},
        models.URLField : {"widget" : forms.URLInput(attrs={"size":100})},
    }
    model = BlogCitation
    can_delete = True
    extra = 0


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    readonly_fields = ["category_slug","created_at","updated_at"]
    search_fields = ["id", "meta_title", "url_slug"]
    list_filter = ["status","category"]
    list_display = ["url_slug","blog_url","category","status"]
    date_hierarchy = "updated_at"
    formfield_overrides = {
        models.CharField : {"widget" : forms.TextInput(attrs={"size":100})},
        models.URLField : {"widget" : forms.URLInput(attrs={"size":100})},
    }
    inlines = [
        BlogAboutInline,
        BlogMentionInline,
        BlogCitationInline
    ]

    def blog_url(self, obj):
        if obj.url_slug == "guides":
            url = "/guides/"
        else:
            url = reverse("guides:blog_url",args=[obj.url_slug])
        return format_html(f"<a href='{url}' target='_blank'>{url}</a>")

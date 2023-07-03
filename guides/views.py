from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.urls import reverse
from .models import *
from bs4 import BeautifulSoup
from .utils import generateWebPageSchema
from web_app.utils import renderTemplate
from django.utils.html import strip_tags
from django.db.models import Count
from django.conf import settings
from django.core.paginator import Paginator


class FormatBlogsObj:
    def formatBlogs(self, blogs_obj):
        formatted_blogs = []
        for blog in blogs_obj:
            temp = {}
            content = blog.content
            soup = BeautifulSoup(content, 'html.parser')
            temp["title"] = blog.meta_title
            temp["img"] = self.getImg(soup)
            if not temp["img"] and blog.featured_image:
                temp["img"] = blog.featured_image.url
            temp["img_alt"] = self.getImgAlt(temp["img"])
            temp["link"] = reverse("guides:blog_url",args=[blog.url_slug])
            temp["category"] = blog.category
            temp["category_slug"] = blog.category_slug
            temp["date"] = blog.created_at
            temp["author"] = blog.created_by
            temp["description"] = strip_tags(str(soup))
            if temp["title"] and temp["img"]:
                formatted_blogs.append(temp)
        return formatted_blogs

    def getImg(self,soup):
        images = soup.select("img")        
        for img in images:
            if img.get("src"):
                img = img["src"]
                return img
        return None
    
    def getImgAlt(self,img_url):
        alt_text = None
        if img_url:
            img_url = img_url.split("/")[-1]
            alt_text = img_url.split(".")[0]
        return alt_text



class HomePageView(TemplateView, FormatBlogsObj):
    template_name = "guides/home_page.html"
    extra_context = {}

    def get(self, *args, **kwargs):
        category_slug = kwargs.get("category_slug")
        if category_slug:
            self.request.extra_context = {"page_url" : "articles/{{x}}"}
            all_blogs = Blog.objects.filter(category_slug=category_slug, content__icontains="<img").order_by("-created_at")
        else:
            self.request.extra_context = {"page_url" : "articles"}
            all_blogs = Blog.objects.all().order_by("-created_at")
        if not all_blogs:
            raise Http404
        
        all_formatted_blogs = self.formatBlogs(all_blogs)
        paginator = Paginator(all_formatted_blogs, settings.ARTICLES_PAGINATION_LIMIT)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        latest_blog_obj = Blog.objects.filter(status="published").order_by("-created_at")[:settings.RECENT_ARTICLES_LIMIT]
        self.extra_context["page_obj"] = page_obj
        self.extra_context["latest_blogs"] = self.formatBlogs(latest_blog_obj)
        self.extra_context["categories"] = Blog.objects.values("category","category_slug").annotate(count=Count("category_slug")).filter(category__isnull=False, content__icontains="<img").order_by("-count")[:settings.TOP_CATEGORIES_LIMIT]
        self.extra_context["category"] = all_blogs.first().category
        self.extra_context["category_slug"] = category_slug
        self.request.extra_context["context"] = self.extra_context.copy()
        return super().get(*args, **kwargs)


class BlogView(TemplateView, FormatBlogsObj):
    template_name = "guides/blog_page.html"
    extra_context = {}


    def get(self, *args, **kwargs):
        url_slug = kwargs.get("url_slug")
        blog_obj = get_object_or_404(Blog, url_slug=url_slug,status="published")
        self.extra_context["blog_obj"] = blog_obj
        latest_blog_obj = Blog.objects.filter(status="published").order_by("-created_at")[:settings.RECENT_ARTICLES_LIMIT]
        self.extra_context["latest_blogs"] = self.formatBlogs(latest_blog_obj)
        
        url_prefix = f"{self.request.scheme}://{self.request.get_host()}"
        self.extra_context["meta_title"] = blog_obj.meta_title
        self.extra_context["meta_desc"] = blog_obj.meta_desc
        soup = BeautifulSoup(blog_obj.content, 'html.parser')
        first_img = self.getImg(soup)
        if blog_obj.featured_image:
            self.extra_context["meta_img_url"] = blog_obj.featured_image.url
        elif first_img:
            self.extra_context["meta_img_url"] = first_img
        else:
            self.extra_context["meta_img_url"] = "/static/default_featured_image.jpg"
        
        self.extra_context["web_page_schema"] = generateWebPageSchema(blog_obj,url_prefix)
        self.extra_context["blog_obj"].content = renderTemplate(blog_obj.content, {"toc":blog_obj.toc})
        self.extra_context["categories"] = Blog.objects.values("category","category_slug").annotate(count=Count("category_slug")).filter(category__isnull=False, content__icontains="<img").order_by("-count")[:settings.TOP_CATEGORIES_LIMIT]
        return super().get(*args, **kwargs)

from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from web_app.models import Doctor, Business
from django.utils.text import slugify
from bs4 import BeautifulSoup


class Blog(models.Model):
    STATUS_CHOICE = (
        ("draft", "Draft"), 
        ("published", "Published")
    )
    meta_title = models.CharField(max_length=500)
    meta_desc = models.CharField(max_length=500)
    url_slug = models.SlugField(max_length=500, unique=True)
    content = RichTextUploadingField()
    toc = RichTextUploadingField(verbose_name="Table of Content", null=True, blank=True)
    featured_image = models.ImageField(upload_to="guides_featured_image/",null=True,blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    publisher = models.ForeignKey(Business, on_delete=models.CASCADE)
    created_by = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="blog_created_by")
    reviewed_by = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="blog_reviewed_by")
    reviewed_at = models.DateTimeField()
    auto_gen_toc = models.BooleanField(verbose_name="Auto Generate Table of Content",default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default="Draft")
    category_slug = models.SlugField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.category:
            self.category_slug = slugify(self.category)
        else:
            self.category_slug = "-"
        if self.auto_gen_toc:
            soup = BeautifulSoup(self.content, 'html.parser')
            all_h2 = soup.select("h2")
            toc_html = '<div class="card toc"> <div class="card-header"> In This Article </div> <div class="card-body">'
            toc_html += '<ul>'
            content = str(soup)
            for h2 in all_h2:
                if h2.text:
                    text = h2.text.strip()
                    text_slug = slugify(text)
                    li_anchor_html = f'<li><a href="#{text_slug}">{text}</a></li>'
                    toc_html += li_anchor_html
                    
                    old_h2 = str(h2).strip()
                    new_h2 = f'<h2 id="{text_slug}">{text}</h2>'
                    content = content.replace(old_h2,new_h2)
            toc_html += "</ul> </div> </div>"
            self.toc = toc_html
            self.content = content
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.url_slug


class BlogMention(models.Model):
    blog=models.ForeignKey(Blog, on_delete=models.CASCADE,related_name="mentions")
    type=models.CharField(max_length=50, default="thing")
    name=models.CharField(max_length=100)
    same_as=models.URLField(max_length=200)


class BlogAbout(models.Model):
    blog=models.ForeignKey(Blog, on_delete=models.CASCADE,related_name="abouts")
    type=models.CharField(max_length=50, default="thing")
    name=models.CharField(max_length=100)
    same_as=models.URLField(max_length=200)


class BlogCitation(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE,related_name="citations")
    headline = models.CharField(max_length=500)
    url = models.URLField(max_length=500)
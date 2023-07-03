import json
from django.urls import reverse
from web_app.utils import getAlumniOf, getExpertise, getPublisher
from bs4 import BeautifulSoup
from django.utils.html import strip_tags


def getReviewedBy(blog_obj, url_prefix):
    doctor_obj = blog_obj.reviewed_by
    doctor_url = url_prefix + reverse("web_app:doctor_url", args=[doctor_obj.slug])
    return [
        {
            "@type": "Person",
            "name": doctor_obj.name,
            "url": doctor_url,
            "honorificPrefix": doctor_obj.honorific_prefix,
            "honorificSuffix": doctor_obj.honorific_suffix,
            "description": strip_tags(doctor_obj.description),
            "knowsAbout": getExpertise(doctor_obj),
            "alumniOf": getAlumniOf(doctor_obj),
            "sameAs": list(doctor_obj.social_links.values_list("url",flat=True))
        }
    ]


def getAllImages(soup):
    img = soup.select("img")
    images = []
    for i in img:
        if i.get("src"):
            image_schema = {
                "@type": "ImageObject",
                "url": i["src"]
            }
            if i.get("alt"):
                image_schema["caption"] = i["alt"]
            if i.get("width"):
                image_schema["width"] = i["width"]  
            if i.get("height"):
                image_schema["height"] = i["height"]  
            images.append(image_schema)
    return images


def getAuthor(blog_obj, url_prefix):
    doctor_obj = blog_obj.created_by
    doctor_url = url_prefix + reverse("web_app:doctor_url", args=[doctor_obj.slug])
    return {
        "@type": "Person",
        "name": doctor_obj.name,
        "url": doctor_url,
        "description": doctor_obj.description,
        "knowsAbout": getExpertise(doctor_obj),
        "alumniOf": getAlumniOf(doctor_obj),
        "sameAs": list(doctor_obj.social_links.values_list("url",flat=True))
    }


def getAbouts(blog_obj):
    abouts_list = []
    for about in blog_obj.abouts.all():
        abouts_list.append({
            "@type": about.type,
            "name": about.name,
            "sameAs": about.same_as
        })
    return abouts_list


def getMentions(blog_obj):
    mentions_list = []
    for mention in blog_obj.mentions.all():
        mentions_list.append({
            "@type": mention.type,
            "name": mention.name,
            "sameAs": mention.same_as
        })
    return mentions_list


def getCitations(blog_obj):
    citations_list = []
    for citation in blog_obj.citations.all():
        citations_list.append({
            "@type": "CreativeWork",
            "citation": citation.headline,
            "headline": citation.headline,
            "url": citation.url
        })
    return citations_list


def getAbout(blog_obj, url_prefix):
    soup = BeautifulSoup(blog_obj.content, 'html.parser')
    article_url = url_prefix + reverse("guides:blog_url", args=[blog_obj.url_slug])
    about_schema = {
        "@type": "MedicalWebPage",
        "url": article_url,
        "headline": blog_obj.meta_title,
        "description": blog_obj.meta_desc,
        "datePublished": blog_obj.created_at.isoformat(),
        "lastReviewed": blog_obj.reviewed_at.isoformat(),
        "dateModified": blog_obj.updated_at.isoformat(),
        "inLanguage": "en-US",
        "image": getAllImages(soup),
        "author": getAuthor(blog_obj,url_prefix),
    }
    
    if blog_obj.citations.all():
        about_schema["citation"] = getCitations(blog_obj)
    if blog_obj.abouts.all():
        about_schema["about"] = getAbouts(blog_obj)
    if blog_obj.mentions.all():
        about_schema["mentions"] = getMentions(blog_obj)

    about_schema["publisher"] = getPublisher(blog_obj.publisher)
    return about_schema



def generateWebPageSchema(blog_obj, url_prefix):
    person_schema_body = {
        "@context": "https://schema.org",
        "@type": [
            "WebPage"
        ]
    }
    
    person_schema_body["reviewedBy"] = getReviewedBy(blog_obj, url_prefix)
    person_schema_body["about"] = getAbout(blog_obj, url_prefix)

    person_schema = '<script type="application/ld+json">'
    person_schema += json.dumps(person_schema_body)
    person_schema += '</script>'
    return person_schema

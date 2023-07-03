from .utils import renderTemplate
from .models import Business, CustomPageContent, CustomSiteContent, Service
from guides.models import Blog
from django.conf import settings


def global_context(request):
    global_context = {}
    
    business = Business.objects.prefetch_related('openinghours_set','adress_set', 'contactpoint_set').get(type="Physician")
    # for footer
    oh = business.openinghours_set.all()
    add = business.adress_set.all()
    ct = business.contactpoint_set.all()
    services = Service.objects.filter(status="published")[:settings.SERVICES_IN_FOOTER_LIMIT]
    context = {"oh": oh, "add": add, "ct": ct, "map_id":business.hasMap,"six_services_obj":services}
    global_context.update(context)

    custom_site_content_obj = CustomSiteContent.objects.filter(status="published")
    if custom_site_content_obj:
        custom_site_content_obj = custom_site_content_obj.first()
        global_context["custom_site_content_obj"] = custom_site_content_obj
        custom_site_content_obj.nav_brand_html = renderTemplate(custom_site_content_obj.nav_brand_html,{"site_name":custom_site_content_obj.site_name,"site_logo":custom_site_content_obj.logo.url})
        custom_site_content_obj.nav_html = renderTemplate(custom_site_content_obj.nav_html,{"ct":ct,"nav_icon_html":custom_site_content_obj.nav_icon_html})
        custom_site_content_obj.footer_html = renderTemplate(custom_site_content_obj.footer_html,{"social_links_html":custom_site_content_obj.social_links_html})
        global_context["site_name"] = custom_site_content_obj.site_name
        global_context["site_url"] = custom_site_content_obj.site_url
        global_context["site_favicon"] = custom_site_content_obj.favicon.url
    
    global_context["cover_img_title"] = request.path.strip("/").split("/")[-1].replace("-"," ").title()
    try:
        extra_context = request.extra_context
        req_context = extra_context.get("context",{})
        page_url = extra_context.get("page_url")
        custom_page_obj = CustomPageContent.objects.get(url=page_url,status="published")
        if req_context:
            global_context["meta_title"] = renderTemplate(custom_page_obj.meta_title, req_context)
            global_context["meta_desc"] = renderTemplate(custom_page_obj.meta_desc, req_context)
        else:
            global_context["meta_title"] = custom_page_obj.meta_title
            global_context["meta_desc"] = custom_page_obj.meta_desc
        if custom_page_obj.featured_image:
            global_context["meta_img_url"] = custom_page_obj.featured_image.url
        else:
            global_context["meta_img_url"] = "/static/default_featured_image.jpg"
        if custom_page_obj.top_img_heading:
            global_context["cover_img_title"] = renderTemplate(custom_page_obj.top_img_heading,req_context)
    except:
        pass
    global_context["top_img"] = CustomPageContent.objects.all().first().top_img
    global_context["recent_articles"] = Blog.objects.all().order_by("-created_at")[:settings.RECENT_ARTICLES_IN_FOOTER_LIMIT]
    return global_context

from django.views.generic import TemplateView,ListView
from .utils import *
from .models import *
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.utils.text import Truncator
from django.conf import settings


class HomePageView(TemplateView):
    template_name = "web_app/home.html"
    extra_context = {}

    def get(self, request, *args, **kwargs):
        request.extra_context = {"page_url" : "/"}
        home = HomePage.objects.prefetch_related('testimonial_set',).latest('id')
        self.extra_context["services"] = Service.objects.filter(status="published").values("name","slug","image","image_caption")[:settings.SERVICES_LIMIT]
        self.extra_context["testimonial"] = home.testimonial_set.all()
        self.extra_context["home"] = home
        doctors = Doctor.objects.prefetch_related('social_links').filter(status="published")
        for doctor in doctors:
            doctor.description = Truncator(doctor.description).chars(80, html=True)
            if not doctor.image:
                if doctor.gender == "male":
                    doctor.gender_image = 'default_male_doctor_profile_pic.png'
                else:
                    doctor.gender_image = 'default_female_doctor_profile_pic.png'
        k=CustomPageContent.objects.filter(url="/")
        self.extra_context["customdata"] = k[0]
        self.extra_context["doctors"] = doctors
        self.extra_context["businessSchema"] = generateBusinessSchema(request.build_absolute_uri())
        return super().get(request, *args, **kwargs)
        


class DoctorPageView(TemplateView):
    template_name = "web_app/doctor_page.html"
    extra_context = {}

    def get(self, request, *args, **kwargs):
        request.extra_context = {"page_url" : "doctors/{{x}}"}
        doctor_slug = kwargs.get("doctor_slug","null")
        doctor_obj = get_object_or_404(Doctor,slug=doctor_slug,status="published")
        url_prefix = f"{request.scheme}://{request.get_host()}"
        doctor_image_caption = doctor_obj.name
        if doctor_obj.image:
            doctor_image_url = doctor_obj.image.url
            doctor_image_caption = doctor_obj.image_caption
        elif doctor_obj.gender == "male":
            doctor_image_url = f"{url_prefix}/static/default_male_doctor_profile_pic.png"
        else:
            doctor_image_url = f"{url_prefix}/static/default_female_doctor_profile_pic.png"
        self.extra_context["doctor_obj"] = doctor_obj
        self.extra_context["meta_img_url"] = doctor_image_url
        self.extra_context["doctor_image_caption"] = doctor_image_caption
        self.extra_context["doctor_schema"] = generatePersonSchemaForDoctor(doctor_obj,url_prefix,doctor_image_url,doctor_image_caption)
        doctor_dict = doctor_obj.__dict__
        doctor_profile_table_data = [
            ("Specializations", doctor_dict["job_title"]),
            ("Expertise", ", ".join(doctor_obj.expertise.values_list("name",flat=True))),
            ("Occupation", f"{doctor_obj.occupations.first().name.title()} ({doctor_obj.occupations.first().description})"),
        ]
        self.extra_context["doctor_profile_table_data"] = doctor_profile_table_data
        self.extra_context["doctor_extra_informations"] = doctor_obj.extra_informations.filter(visibility=True).order_by("ordering")
        k=CustomPageContent.objects.filter(url="doctors/{{x}}")
        self.extra_context["customdata"] = k[0]


        all_doctors = Doctor.objects.prefetch_related('social_links').filter(status="published")
        for doctor in all_doctors:
            doctor.description = Truncator(doctor.description).chars(80, html=True)
            if not doctor.image:
                if doctor.gender == "male":
                    doctor.gender_image = 'default_male_doctor_profile_pic.png'
                else:
                    doctor.gender_image = 'default_female_doctor_profile_pic.png'
        self.extra_context["all_doctors"] = all_doctors

        request.extra_context["context"] = self.extra_context.copy()
        return super().get(request, *args, **kwargs)
    

def contact(request):
    request.extra_context = {"page_url" : "contact-us"}
    business = Business.objects.prefetch_related('openinghours_set', 'adress_set', 'contactpoint_set',).get(type="Physician")

    oh = business.openinghours_set.all()
    add = business.adress_set.all()
    ct = business.contactpoint_set.all()

    if request.POST:
        name = request.POST["name"]
        email = request.POST["email"]
        message = request.POST["message"]
        question = Question(name=name,email=email,comment=message)
        question.save()
    k=CustomPageContent.objects.filter(url="contact-us")

    context = {"oh":oh,"add":add,"ct":ct,"map":business.map_id,"customdata":k[0]}
    context["businessSchema"] = generateBusinessSchema(request.build_absolute_uri())
    request.extra_context["context"] = context
    return render(request,"web_app/contact.html",context)


def services(requests,service_name):
    requests.extra_context = {"page_url" : "services/{{x}}"}
    service_obj = get_object_or_404(Service,slug=service_name,status="published")
    provider_obj = Business.objects.all().first()
    k=CustomPageContent.objects.filter(url="services/{{x}}")
    context={
        "service_obj":service_obj,
        "provider":provider_obj.map_id,
        "contact_number":provider_obj.contactpoint_set.all().first().telephone,
        "all_services": Service.objects.all(),
        "service_name":service_name,
        "customdata":k[0]
    }

    requests.extra_context["context"] = context
    return render(requests,template_name="web_app/service_page.html",context=context)


class about_us(ListView):
    model = Doctor
    template_name="web_app/about_page.html"
    paginate_by=4
    context_object_name="docdata"
    extra_context = {}

    def get(self, request, *args, **kwargs):
        request.extra_context = {"page_url" : "about-us"}
        k=CustomPageContent.objects.filter(url="about-us")
        self.extra_context["customdata"] = k[0]
        self.extra_context["businessSchema"] = generateBusinessSchema(request.build_absolute_uri())
        request.extra_context["context"] = self.extra_context.copy()
        return super().get(request, *args, **kwargs)
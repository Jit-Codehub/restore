import json
from django.urls import reverse
from django.template import Template,Context
from django.utils.html import strip_tags
from .models import Business,Doctor,Service


def renderTemplate(content,context):
    template = Template(content)
    context = Context(context)
    content = template.render(context)
    return content


def getAlumniOf(doctor_obj):
    result = []
    for alumni in doctor_obj.alumni.all():
        temp = {
            "@type": "CollegeOrUniversity",
            "name": alumni.name,
            "sameAs": alumni.url
        }
        result.append(temp)
    return result


def getDoctor(doctors_obj):
    result = []
    for doctor in doctors_obj:
        doctor_url = reverse("web_app:doctor_url", args=[doctor.slug])
        temp = {
            "@type": "Person",
            "@id": doctor_url,
            "name": doctor.name
        }
        result.append(temp)
    return result


def getColleagues(colleagues_obj, url_prefix):
    result = []
    for obj in colleagues_obj:
        colleague_doctor_obj = obj.colleague
        colleague_url = url_prefix + reverse("web_app:doctor_url", args=[colleague_doctor_obj.slug])
        temp = {
            "@type": "Person",
            "@id": colleague_url,
            "name": colleague_doctor_obj.name
        }
        result.append(temp)
    return result


def getCredentials(doctor_obj):
    result = []
    for credential in doctor_obj.credentials.all():
        temp = {
            "@type": "EducationalOccupationalCredential",
            "credentialCategory": credential.category,
            "name": credential.name,
            "url": credential.url
        }
        result.append(temp)
    return result

def getOccupations(doctor_obj):
    result = []
    for occupation in doctor_obj.occupations.all():
        temp = {
            "@type": "Occupation",
            "name": occupation.name,
            "occupationalCategory": occupation.category,
            "description": occupation.description
        }
        result.append(temp)
    return result

def getExpertise(doctor_obj):
    result = []
    for expertise in doctor_obj.expertise.all():
        if expertise.type == "text":
            result.append(expertise.name)
        else:
            temp =  {
                "@type": "Thing",
                "name": expertise.name,
                "sameAs": expertise.url
            }
            result.append(temp)
    return result

def getMemberOf(doctor_obj):
    result = []
    for organizations in doctor_obj.member_of_organizations.all():
        temp = {
            "@type": "MedicalOrganization",
            "name": organizations.name,
            "sameAs": organizations.url
        }
        result.append(temp)
    return result

def getWorksFor(doctor_obj):
    result = []
    for organizations in doctor_obj.works_for_organizations.all():
        temp = {
            "@type": "MedicalOrganization",
            "name": organizations.name,
            "sameAs": organizations.url
        }
        result.append(temp)
    return result

def getImage(doctor_image_url,doctor_image_caption):
    return {
        "@type": "ImageObject",
        "url": doctor_image_url,
        "caption": doctor_image_caption
    }

def getPublisher(business_obj):
    l_adress = []
    for i in business_obj.adress_set.all():
        d = {}
        if i.type:
            d['@type'] = i.type
        if i.postalCode:
            d['postalCode'] = i.postalCode
        if i.addressRegion:
            d['addressRegion'] = i.addressRegion
        if i.addressCountry:
            d['addressCountry'] = i.addressCountry
        if i.streetAddress:
            d['streetAddress'] = i.streetAddress
        if i.addressLocality:
            d['addressLocality'] = i.addressLocality
        l_adress.append(d)

    l_contactPoint = []
    d = {}
    for i in business_obj.contactpoint_set.all():
        d["name"] = Doctor.objects.all().first().name
        if i.type:
            d['@type'] = i.type
        if i.contactType:
            d['contactType'] = i.contactType
        if i.telephone:
            d['telephone'] = i.telephone
        break
    l_contactPoint = d

    return {
        "@type": "Organization",
        "@id": business_obj.url,
        "name": business_obj.name,
        "logo":business_obj.logo.url,
        "description":business_obj.description,
        "knowsLanguage":list(business_obj.knows_language.values_list("language",flat=True)),
        "contactPoint": l_contactPoint,
        "address": l_adress,
        "sameAs": business_obj.SameAs,
    }


def generatePersonSchemaForDoctor(doctor_obj, url_prefix,doctor_image_url,doctor_image_caption):
    doctor_url = url_prefix + reverse("web_app:doctor_url", args=[doctor_obj.slug])
    person_schema_body = {
        "@context": "https://schema.org",
        "@type": [
            "Person",
            "WebPage"
        ],
        "@id": doctor_url,
        "additionalName": doctor_obj.additional_name,
    }
    person_schema_body["alumniOf"] = getAlumniOf(doctor_obj)
    person_schema_body["award"] = list(doctor_obj.awards.values_list("name",flat=True))
    colleagues_obj = doctor_obj.colleagues.all()
    if colleagues_obj:
        person_schema_body["colleague"] = getColleagues(colleagues_obj,url_prefix)
    if doctor_obj.family_name:
        person_schema_body["familyName"] = doctor_obj.family_name
    if doctor_obj.given_name:
        person_schema_body["givenName"] = doctor_obj.given_name
    person_schema_body["gender"] = doctor_obj.gender
    if doctor_obj.credentials.all():
        person_schema_body["hasCredential"] = getCredentials(doctor_obj)
    person_schema_body["hasOccupation"] = getOccupations(doctor_obj)
    person_schema_body["honorificPrefix"] = doctor_obj.honorific_prefix
    if doctor_obj.honorific_suffix:
        person_schema_body["honorificSuffix"] = doctor_obj.honorific_suffix
    person_schema_body["jobTitle"] = doctor_obj.job_title
    person_schema_body["knowsAbout"] = getExpertise(doctor_obj)
    if doctor_obj.knows_languages.all():
        person_schema_body["knowsLanguage"] = list(doctor_obj.knows_languages.values_list("name",flat=True))
    person_schema_body["memberOf"] = getMemberOf(doctor_obj)
    person_schema_body["worksFor"] = getWorksFor(doctor_obj)
    person_schema_body["additionalType"] = doctor_obj.additional_type
    person_schema_body["description"] = strip_tags(doctor_obj.description)
    person_schema_body["disambiguatingDescription"] = doctor_obj.disambiguating_description
    person_schema_body["image"] = getImage(doctor_image_url,doctor_image_caption)
    person_schema_body["name"] = doctor_obj.name
    person_schema_body["url"] = doctor_url
    person_schema_body["sameAs"] = list(doctor_obj.social_links.values_list("url",flat=True))
    person_schema_body["isPartOf"] = doctor_obj.is_part_of
    person_schema_body["publisher"] = getPublisher(doctor_obj.publisher)

    person_schema = '<script type="application/ld+json">'
    person_schema += json.dumps(person_schema_body)
    person_schema += '</script>'
    return person_schema




def generateBusinessSchema(absolute_uri):
    business = Business.objects.prefetch_related('curreny_Accepted', 'knows_language', 'haspart_set', 'openinghours_set',
                                                 'adress_set', 'geo_set', 'areaserved_set', 'contactpoint_set', 'image_set').get(type="Physician")

    l_availableService = []
    for obj in Service.objects.all():
        d = {}
        d['@id'] = reverse("web_app:services",args=[obj.slug])
        d['@type'] = "MedicalProcedure"
        d[f'name'] = obj.name
        if obj.additional_type:
            d['sameAs'] = obj.additional_type
        d['description'] = obj.description
        l_availableService.append(d)

    openhours = ''
    for i in business.openinghours_set.all():
        if i.day:
            openhours += i.day+" "
        if i.timming:
            openhours += i.timming+"  "

    l_adress = []
    for i in business.adress_set.all():
        d = {}
        if i.type:
            d['@type'] = i.type
        if i.postalCode:
            d['postalCode'] = i.postalCode
        if i.addressRegion:
            d['addressRegion'] = i.addressRegion
        if i.addressCountry:
            d['addressCountry'] = i.addressCountry
        if i.streetAddress:
            d['streetAddress'] = i.streetAddress
        if i.addressLocality:
            d['addressLocality'] = i.addressLocality
        l_adress.append(d)

    l_geo = []
    for i in business.geo_set.all():
        d = {}
        if i.type:
            d['@type'] = i.type
        if i.name:
            d['name'] = i.name
        if i.postalCode:
            d['postalCode'] = i.postalCode
        if i.latitude:
            d['latitude'] = i.latitude
        if i.longitude:
            d['longitude'] = i.longitude
        if i.description:
            d['description'] = i.description

        l_geo.append(d)

    l_areaServed = []
    for i in business.areaserved_set.all():
        d = {}
        if i.type:
            d['@type'] = i.type
        if i.name:
            d['name'] = i.name
        if i.url:
            d['@id'] = i.url

        l_areaServed.append(d)

    l_contactPoint = []
    d = {}
    for i in business.contactpoint_set.all():
        d["name"] = Doctor.objects.all().first().name
        if i.type:
            d['@type'] = i.type
        if i.contactType:
            d['contactType'] = i.contactType
        if i.telephone:
            d['telephone'] = i.telephone
        break
    l_contactPoint = d


    l_image = []
    for i in business.image_set.all():
        d = {}
        if i.type:
            d['@type'] = i.type
        if i.name:
            d['name'] = i.name
        if i.url:
            d['url'] = i.url.url
        if i.creator:
            d['creator'] = i.creator
        if i.contentLocation:
            d['contentLocation'] = i.contentLocation

        l_image.append(d)

    l_haspart = []
    for i in business.haspart_set.all():
        d = {}
        if i.type:
            d['@type'] = i.type
        if i.url:
            d['@id'] = i.url

        l_haspart.append(d)

    businessSchema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@context": "https://schema.org",
                "@type": business.type,
                "@id": business.map_id,
                "additionalType": business.additional_Type,
                "availableService": l_availableService,
                "medicalSpecialty": business.medical_Specialty,
                "currenciesAccepted": [i.currencyName for i in business.curreny_Accepted.all()],
                "openingHours":openhours,
                "paymentAccepted":business.payment_Accepted,
                "address":l_adress,
                "geo":l_geo,
                "hasMap":business.hasMap,
                "logo":business.logo.url,
                "telephone":business.telephone,
                "isAcceptingNewPatients":business.isAcceptingNewPatients,
                "areaServed":l_areaServed,
                "contactPoint":l_contactPoint,
                "employee":getDoctor(Doctor.objects.all()),
                "knowsLanguage":[i.language for i in business.knows_language.all()],
                "image":l_image,
                "url":business.url,
                "name":business.name,
                "alternateName":[business.AlternateName],
                "description":business.description,
                "disambiguatingDescription":business.disambiguatingDescription,
                "foundingDate":business.foundingDate,
                "sameAs":[business.SameAs]
            },
            {
                "@type": "Website",
                "publisher": {
                    "@id": business.map_id
                },
                "name": business.name,
                "@id": absolute_uri,
                "url": business.url,
                "hasPart": l_haspart,
            }
        ]
    }

    business_Schema = '<script type="application/ld+json">'
    business_Schema += json.dumps(businessSchema)
    business_Schema += '</script>'
    return business_Schema
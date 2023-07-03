from django.db import models
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError


class CustomSiteContent(models.Model):
    STATUS_CHOICE = (
        ("draft", "Draft"),
        ("published", "Published")
    )
    site_name = models.CharField(max_length=255)
    site_url = models.CharField(max_length=255)
    logo = models.ImageField(upload_to="logo/")
    favicon = models.ImageField(upload_to="logo/")
    nav_brand_html = RichTextUploadingField()
    nav_html = RichTextUploadingField()
    footer_html = RichTextUploadingField(null=True, blank=True)
    nav_icon_html = models.CharField(max_length=255, null=True, blank=True)
    social_links_html = models.TextField(null=True, blank=True)
    script = models.TextField(null=True, blank=True)
    copyright_text = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default="draft")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.site_name} - {self.status}"


class CustomPageContent(models.Model):
    STATUS_CHOICE = (
        ("draft", "Draft"),
        ("published", "Published")
    )
    url = models.CharField(max_length=255, unique=True)
    meta_title = models.CharField(max_length=255)
    meta_desc = models.CharField(max_length=255)
    featured_image = models.ImageField(upload_to="featured_images/", null=True, blank=True)
    top_img = models.ImageField(upload_to='images', null=True, blank=True)
    top_img_heading = models.CharField(max_length=255, null=True, blank=True)

    notice=RichTextUploadingField(blank=True)
    displayimage=models.ImageField(upload_to='images', null=True, blank=True)
    aboutDescript=RichTextUploadingField(null=True, blank=True)
    meetteam=RichTextUploadingField(null=True, blank=True)
    afterTeamContent=RichTextUploadingField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default="draft")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.url

    def clean(self) -> None:
        self.url = self.url.strip("/") if self.url != "/" else self.url
        if not self.url:
            raise ValidationError("URL should not be empty or invalid URL")
        

class HomePage(models.Model):
    image = models.ImageField(upload_to='homepage/', verbose_name='large image')
    text = models.TextField(verbose_name='text on lagre image')
    about_us_heading = models.CharField(max_length=255, default='About Us')
    about_us_image = models.ImageField(upload_to='homepage/',verbose_name='about-us image')
    # about_us_text = models.TextField(verbose_name='about-us text')
    about_us_text = RichTextField(verbose_name='about-us text')
    service_heading = models.CharField(max_length=255, default='SERVICES')
    service_subheading = models.CharField(max_length=255, default='Excellent Medical Services')
    doctor_heading = models.CharField(max_length=255, default='Meet Our Team')
    doctor_subheading = models.CharField(max_length=255, default='Qualified Healthcare Professionals')
    testimonial_heading = models.CharField(max_length=255, default='TESTIMONIAL')
    testimonial_subheading = models.CharField(max_length=255, default='Patients Say About Our Services')

    def __str__(self):
        self.heading = "Home Page Data"
        return self.heading


# class HomePageServices(models.Model):
#     image = models.ImageField(upload_to='homepage/services')
#     imageTitle = models.CharField(max_length=255)
#     homePage = models.ForeignKey(HomePage, on_delete=models.CASCADE) 

class TESTIMONIAL(models.Model):
    image = models.ImageField(upload_to='homepage/testimonial',null=True,blank=True)
    Comment = models.TextField()
    customerName = models.CharField(max_length=255)
    homePage = models.ForeignKey(HomePage, on_delete=models.CASCADE)





######################################## Business Schema ########################################
STATUS_CHOICE = (
    ("Sunday", "Sunday"),
    ("Monday", "Monday"),
    ("Tuesday", "Tuesday"),
    ("Wednesday", "Wednesday"),
    ("Thursday", "Thursday"),
    ("Friday", "Friday"),
    ("Saturday", "Saturday"),
)

STATUS_PATIENT = (
    ("True", "True"),
    ("False", "False"),
)

class Currency(models.Model):
    currencyName = models.CharField(max_length=255)

    def __str__(self):
        return self.currencyName
    
class KnowsLanguage(models.Model):
    language = models.CharField(max_length=255)

    def __str__(self):
        return self.language


class Business(models.Model):

    type = models.CharField(max_length=255)
    map_id = models.URLField(max_length=1000)
    additional_Type = models.URLField(blank=True,null=True)
    medical_Specialty = models.CharField(max_length=255)
    curreny_Accepted = models.ManyToManyField(Currency)
    payment_Accepted = models.CharField(max_length=255)
    hasMap = models.URLField(max_length=1000)
    logo = models.ImageField(upload_to='logo/')
    telephone = models.CharField(max_length=255,blank=True,null=True)
    isAcceptingNewPatients = models.CharField(max_length=255, choices=STATUS_PATIENT,default='yes')
    knows_language = models.ManyToManyField(KnowsLanguage)
    url = models.URLField()
    name = models.CharField(max_length=255)
    AlternateName = models.CharField(max_length=255,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    disambiguatingDescription = models.TextField(blank=True,null=True)
    foundingDate = models.CharField(max_length=255)
    SameAs = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.type

class Haspart(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, default="CreativeWork")
    url = models.URLField()

class OpeningHours(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    day = models.CharField(max_length=255, choices=STATUS_CHOICE)
    timming = models.CharField(max_length=255)

class Adress(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, default="PostalAddress")
    type = models.CharField(max_length=255)
    postalCode = models.CharField(max_length=255)
    addressRegion = models.CharField(max_length=255)
    addressCountry = models.CharField(max_length=255)
    streetAddress = models.CharField(max_length=500)
    addressLocality = models.CharField(max_length=500)

class Geo(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    type = models.CharField(max_length=255,default="GeoCoordinates")
    name = models.CharField(max_length=255)
    postalCode = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)

class AreaServed(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, default="City")
    name = models.CharField(max_length=255)
    url = models.URLField()

class ContactPoint(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    type = models.CharField(max_length=255,default="ContactPoint")
    contactType = models.CharField(max_length=255)
    telephone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

class Image(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    type = models.CharField(max_length=255,default="ImageObject")
    name = models.CharField(max_length=255)
    url = models.ImageField(upload_to='images/')
    creator = models.CharField(max_length=255)
    contentLocation = models.CharField(max_length=255)



class Question(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name




######################################## Doctor Schema ########################################
class Doctor(models.Model):
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female")
    )
    STATUS_CHOICE = (
        ("draft", "Draft"), 
        ("published", "Published")
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    additional_name = models.CharField(max_length=255, null=True, blank=True)
    family_name = models.CharField(max_length=255, null=True, blank=True)
    given_name = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default="male")
    image = models.ImageField(upload_to="doctor_images/", null=True, blank=True)
    image_caption = models.CharField(max_length=255, null=True, blank=True)
    honorific_prefix = models.CharField(max_length=20, default="Dr.")
    honorific_suffix = models.CharField(max_length=20, null=True, blank=True)
    job_title = models.CharField(max_length=255)
    description = RichTextField()
    disambiguating_description = models.CharField(max_length=255, null=True, blank=True)
    additional_type = models.CharField(max_length=255, null=True, blank=True)
    is_part_of = models.URLField(null=True, blank=True)
    publisher = models.ForeignKey(Business, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default="Draft")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        if self.honorific_suffix and self.honorific_suffix not in self.name:
            return f"{self.name}, {self.honorific_suffix}"
        else:
            return self.name



class DoctorSocialLinks(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="social_links")
    name = models.CharField(max_length=255)
    url = models.URLField()

    class Meta:
        verbose_name = "Social Link"
        verbose_name_plural = "Social Links"
        

class DoctorAlumni(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="alumni")
    program_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255, verbose_name="college/university name")
    url = models.URLField()

    def save(self, *args, **kwargs):
        if not self.program_name and self.url:
            self.program_name = self.url.strip("/").split("/")[-1].split(".")[0].title().replace("-"," ")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Alumni College or University"
        verbose_name_plural = "Alumni College or University"
        

class DoctorAward(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="awards")
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Award"
        verbose_name_plural = "Awards"


class DoctorColleague(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="colleagues")
    colleague = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Colleague"
        verbose_name_plural = "Colleagues"


class DoctorEducationalOccupationalCredential(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="credentials")
    category = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    url = models.URLField()

    class Meta:
        verbose_name = "Educational Occupational Credential"
        verbose_name_plural = "Educational Occupational Credentials"


class DoctorOccupation(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="occupations")
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        verbose_name = "Occupation"
        verbose_name_plural = "Occupations"


class DoctorExpertise(models.Model):
    TYPE_CHOICES = (
        ("text", "Text"),
        ("thing", "Thing")
    )
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="expertise")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="text")
    name = models.CharField(max_length=255)
    url = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name = "Expertise"
        verbose_name_plural = "Expertise"


class DoctorKnowsLanguage(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="knows_languages")
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Knows Language"
        verbose_name_plural = "Knows Languages"


class DoctorMemberOfOrganization(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="member_of_organizations")
    name = models.CharField(max_length=255)
    url = models.URLField()

    class Meta:
        verbose_name = "Member of Organization"
        verbose_name_plural = "Member of Organizations"


class DoctorWorksForOrganization(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="works_for_organizations")
    name = models.CharField(max_length=255)
    url = models.URLField()
    position = models.CharField(max_length=255, null=True, blank=True)
    year_range = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Works for Organization"
        verbose_name_plural = "Works for Organizations"


class DoctorExtraInformation(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="extra_informations")
    heading = models.CharField(max_length=255)
    body = RichTextUploadingField()
    ordering = models.PositiveIntegerField(default=1)
    visibility = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Extra Information"
        verbose_name_plural = "Extra Informations"





######################################## Service Schema ########################################


class Service(models.Model):
    STATUS_CHOICE = (
        ("draft", "Draft"), 
        ("published", "Published")
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    type = models.CharField(max_length=255)
    additional_type= models.CharField(max_length=255, null=True, blank=True, help_text="https://en.wikipedia.org/wiki/Clear_aligners")
    brand= models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    disambiguating_description = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='images')
    image_caption = models.CharField(max_length=255)
    potential_action = models.CharField(max_length=255, null=True, blank=True, help_text="Call for a free consultation")
    is_part_of=models.URLField(max_length=255, default="https://soumyahospitals.com")
    reviewed_by = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="service_reviewed_by")
    content = RichTextUploadingField(help_text="content will display in frontend only")
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default="Draft")

    def __str__(self):
        return self.name

class ServiceMentions(models.Model):
    service=models.ForeignKey(Service, on_delete=models.CASCADE)
    type=models.CharField(max_length=50)
    name=models.CharField(max_length=100)
    same_as=models.URLField(max_length=200)


class ServiceAbout(models.Model):
    service=models.ForeignKey(Service, on_delete=models.CASCADE)
    type=models.CharField(max_length=50)
    name=models.CharField(max_length=100)
    same_as=models.URLField(max_length=200)
    



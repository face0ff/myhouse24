from django.db import models

# Create your models here.


class AditGallery(models.Model):
    adit_image = models.ImageField("Изображение", upload_to="img/", blank=True)


class Gallery(models.Model):
    image = models.ImageField("Изображение", upload_to="img/", blank=True)


class Seo(models.Model):
    titles = models.CharField("Заголовок", max_length=100)
    descriptions = models.CharField("Краткий текст", max_length=200)
    keywords = models.TextField("Текст", max_length=250)


class Service(models.Model):
    seo = models.OneToOneField(Seo, on_delete=models.PROTECT)


class Main(models.Model):
    header = models.CharField("Заголовок", max_length=100)
    description = models.CharField("Краткий текст", max_length=400)
    show_url = models.BooleanField(default=True)
    slider_1 = models.ImageField("Изображение", upload_to="slider/img/")
    slider_2 = models.ImageField("Изображение", upload_to="slider/img/")
    slider_3 = models.ImageField("Изображение", upload_to="slider/img/")
    seo = models.OneToOneField(Seo, on_delete=models.PROTECT)


class Block(models.Model):
    header = models.CharField("Название", max_length=100, null=True, blank=True)
    description = models.TextField("Описание", max_length=200, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    image = models.ImageField("Изображение", upload_to="block/img/")



class Info(models.Model):

    header = models.CharField("Заголовок", max_length=100, null=True, blank=True)
    text = models.TextField("Краткий текст", max_length=200, null=True, blank=True)
    photo = models.ImageField("Изображение", upload_to="slider/img/")
    adit_header = models.CharField("Заголовок", max_length=100, null=True, blank=True)
    adit_text = models.TextField("Краткий текст", max_length=200, null=True, blank=True)
    seo = models.OneToOneField(Seo, on_delete=models.PROTECT)


class Files(models.Model):
    name = models.CharField("Название документа", max_length=100)
    files = models.FileField('PDF, JPG (макс. размер 20 Mb)', upload_to="files/")


class Contacts(models.Model):

    header = models.CharField("Заголовок", max_length=100, null=True, blank=True)
    text = models.TextField("Краткий текст", max_length=200, null=True, blank=True)
    url = models.URLField("Ссылка на комерческий сайт", max_length=200, null=True, blank=True)
    map = models.CharField("Код карты", max_length=200, null=True, blank=True)
    fio = models.CharField("ФИО", max_length=200, null=True, blank=True)
    address = models.CharField("Адрес", max_length=100, null=True, blank=True)
    location = models.CharField("Локация", max_length=500, null=True, blank=True)
    phone = models.CharField("Телефон", max_length=15, null=True, blank=True)
    email = models.CharField("E-mail", max_length=30, null=True, blank=True)
    seo = models.OneToOneField(Seo, on_delete=models.PROTECT)





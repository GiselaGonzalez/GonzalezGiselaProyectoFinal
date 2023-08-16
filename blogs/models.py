from django.db import models
from django.conf import settings
from django.urls import reverse
from ckeditor.fields import RichTextField
# Create your models here.

class Post(models.Model):
    titulo = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    descripcion =models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    contenido = RichTextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    categories = models.ManyToManyField("Category")
    featured = models.BooleanField(default=False)
    imagen = models.ImageField(blank=True, null=True)
    
    def get_absolute_url(self):
        return reverse("blogs:post", kwargs={"slug":self.slug})
    
    class Meta:
        ordering = [ "-fecha_creacion" ]
    def __str__(self):
        return self.titulo 


class Category(models.Model):
    titulo = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "categories"


    def get_absolute_url(self):
        return reverse("blogs:category", kwargs={"slug":self.slug})

    

    def __str__(self):
        return self.titulo
    
class Comentarios(models.Model):
    contenido = models.TextField(max_length=1000, help_text='Ingrese comentarios')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    post_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)


    class Meta:
        ordering = ['-post_date']


    def __str__(self):
        len_title =15
        if len (self.contenido) > len_title:
            return self.contenido[:len_title] + '...'
        return self.contenido
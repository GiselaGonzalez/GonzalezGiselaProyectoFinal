from django.contrib import admin
from blogs.models import Post, Category,Comentarios

# Register your models here.
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comentarios)
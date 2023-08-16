from django import forms

from blogs.models import Comentarios

class PostComentariosForm(forms.ModelForm):
    contenido = forms.CharField(label= 'Ingrese su comentario')

    class Meta:
        model = Comentarios
        fields = ['contenido']
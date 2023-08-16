from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic, View
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse


from blogs.models import Post, Category
from Blog.forms import PostComentariosForm
# Create your views here.

def home_page(request):
    posts = Post.objects.all()
    categorias = Category.objects.all()
    featured = Post.objects.filter(featured=True)[:3]
    


    context = {
        'post_list':posts,
        'categorias':categorias,
        'featured':featured
        

    }
    
    return render(request, 'blogs/home_page.html', context=context)

class PostDetailView(generic.DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(** kwargs)
        context ['form'] = PostComentariosForm()
        return context

class PostComentariosView(LoginRequiredMixin, SingleObjectMixin, FormView):
     template_name = 'blogs/post_detail.html'
     form_class = PostComentariosForm
     model = Post

     def post(self, request, *args, **kwargs):
          self.object = self.get_object()
          return super().post(request, *args, **kwargs)
     
     def form_valid(self, form):
         f = form.save(commit=False)
         f.author = self.request.user
         f.post = self.object
         f.save()
         return super().form_valid(form)
    
     def get_success_url(self):
         
         return reverse('blogs:post', kwargs={'slug': self.object.slug}) + '#comments-section'
         
     


class PostView(View):   

    def get(self, request, *args, **kwargs):
            view = PostDetailView.as_view()
            return view(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
            view = PostComentariosView.as_view()
            return view(request, *args, **kwargs)
    
    
                
class FeaturedListView(generic.ListView):
    model = Post
    template_name = 'blogs/results.html'

    def get_queryset(self):
        query = Post.objects.filter(featured=True)
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(** kwargs)
        context ['categorias'] = Category.objects.all()
        return context
    
class CategoryListView(generic.ListView):
    model = Post
    tempate_name = 'blogs/results.html'  
    
    def get_queryset(self):
        query = self.request.path
        post_list = Post.objects.filter(categories__slug=query)
        return post_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(** kwargs)
        context ['categorias'] = Category.objects.all()
        return context

class SearchResulstViews(generic.ListView):
    model = Post
    tempate_name = 'blogs/results.html'  
    
    def get_queryset(self):
        query = self.request.GET.get('search')
        post_list = Post.objects.filter(
            Q(titulo__icontains=query) | Q( categories__titulo__icontains=query)
        )
        return post_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(** kwargs)
        context ['categorias'] = Category.objects.all()
        return context
    
    
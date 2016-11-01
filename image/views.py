from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from image.models import Image, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse, reverse_lazy

class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = "/"

class ImageCreateView(CreateView):
    model = Image
    success_url = "/"
    fields = ('title', 'description', 'graphic', 'picture')

    def form_valid(self, form):
        instance = form.save(commit = False)
        instance.user = self.request.user
        return super().form_valid(form)

class ImageUpdateView(UpdateView):
    model = Image
    success_url = "/"
    fields = ('title', 'description', 'graphic', 'picture')

class IndexView(ListView):
    model = Image
    paginate_by = 3

class ImageDetailView(DetailView):
    model = Image
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comms = Comment.objects.filter(image=self.kwargs['pk'])
        x = Image.objects.all()
        y = x.get(id=self.kwargs['pk'])
        z = y.id
        next_page = z + 1
        # def next_page_x(self):
        #     q = z + 1
        #     while not x.get(id=q):
        #         q += 1
        #     return q

        prev_page = z - 1
        # def prev_page_x(self):
        #     q = z - 1
        #     while not x.get(id=q):
        #         q -= 1
        #     return q

        def get_left(self):
            if prev_page == 0:
                return False
            left = x.get(id=prev_page)
            return left


        def get_right(self):
            var = x.count() + 1
            if next_page >= var:
                return False
            right = x.get(id=next_page)
            return right
        #left = x.get(id=prev_page)

        context['left'] = get_left(self)
        context['right'] = get_right(self)
        context['prev_page'] = prev_page
        context['next_page'] = next_page
        context['comms'] = comms
        context['x'] = z

        return context


class CommentCreateView(CreateView):
    model = Comment
    fields = ('body',)
    def get_success_url(self, **kwargs):
         target = Image.objects.get(id=self.kwargs['pk'])
         return reverse_lazy('image_detail_view', args=(target.id,))

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.image = Image.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)

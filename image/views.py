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
        prev_page = z - 1
        stopper_end = Image.objects.last().id
        stopper_start = Image.objects.first().id
        
        def next_right_x(self):
            current_id = z
            while current_id < stopper_end:
                current_id += 1
                if x.get(id=current_id):
                    return current_id
            return stopper_start

        def next_left_x(self):
            current_id = z
            while current_id > 1:
                current_id -= 1
                if x.get(id=current_id):
                    return current_id
            return stopper_end


        context['comms'] = comms
        context['left_obj'] = x.get(id=next_left_x(self))
        context['right_obj'] = x.get(id=next_right_x(self))

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

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import BlogModel, AddEbookModel


class BlogListView(ListView):
    model = BlogModel


class BlogDetailView(DetailView):
    model = BlogModel


class AddEbookView(SuccessMessageMixin, CreateView):
    model = AddEbookModel
    fields = ['ebook_title', 'ebook_link', 'full_name', 'email']
    success_message = "Your request has been sent successfully!"

    def get_success_url(self):
        return reverse_lazy('add_book')

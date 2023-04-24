from django.urls import path
from .views import home, filter_ebook_view, EbookDetailView, read_pdf, download_file, read_sale_pdf
from django.views.generic import TemplateView

urlpatterns = [
    path('', home, name='home'),
    path('filter-ebook/', filter_ebook_view, name='filter_ebook'),
    path('about/', TemplateView.as_view(template_name="navigation/about.html"), name='about'),
    path('ebook-detail/<slug:slug>/', EbookDetailView.as_view(), name='ebook_detail'),
    path('read-online/', read_pdf, name='read_pdf'),
    path('read-sale-online/', read_sale_pdf, name='read_sale_pdf'),
    path('download-file/', download_file, name='download_file'),
    path('advertising/', TemplateView.as_view(template_name="advertising.html"), name="advertising"),
]

from django.urls import path
from django.views.generic import TemplateView
from .views import AddEbookView, BlogListView, BlogDetailView

urlpatterns = [
    path('privacy-policy/', TemplateView.as_view(template_name="footer/privacy_policy.html"), name='privacy_policy'),
    path('terms-and-conditions/', TemplateView.as_view(template_name="footer/terms_of_use.html"),
         name='terms_and_conditions'),
    path('disclaimer/', TemplateView.as_view(template_name="footer/disclaimer.html"), name='disclaimer'),
    path('add-ebook/', AddEbookView.as_view(), name='add_book'),
    path('blog/', BlogListView.as_view(), name='blog'),
    path('blog/<slug:slug>', BlogDetailView.as_view(), name='blog_detail'),
]

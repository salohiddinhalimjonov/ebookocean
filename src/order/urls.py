from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .views import CreateStripeCheckoutSessionView, my_ebooks_view

app_name = "order"

urlpatterns = [
    path(
        "create-checkout-session/<slug:slug>/",
        login_required(CreateStripeCheckoutSessionView.as_view(), login_url="sign-in"),
        name="create-checkout-session",
    ),
    path('success/', TemplateView.as_view(template_name="success.html"), name='success'),
    path('cancel/', TemplateView.as_view(template_name="cancel.html"), name='cancel'),
    path('my-ebooks/', my_ebooks_view, name='my_ebooks'),
]
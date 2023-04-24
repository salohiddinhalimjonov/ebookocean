from django.shortcuts import render
import stripe
from django.conf import settings
from django.views import View
from django.shortcuts import redirect
from src.ebook.models import EbookModel
from .models import Order
from django.contrib.auth.decorators import login_required


stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateStripeCheckoutSessionView(View):
    """
    Create a checkout session and redirect the user to Stripe's checkout page
    """

    def post(self, request, *args, **kwargs):
        ebook = EbookModel.objects.get(slug=self.kwargs["slug"])
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": int(ebook.price) * 100,
                        "product_data": {
                            "name": ebook.title,
                            "description": ebook.description,
                            "images": [
                                f"{settings.BACKEND_DOMAIN}/web_images/{ebook.cover_image}"
                            ],
                        },
                    },
                    "quantity": 1,
                }
            ],
            metadata={"product_id": ebook.id},
            mode="payment",
            success_url=settings.PAYMENT_SUCCESS_URL,
            cancel_url=settings.PAYMENT_CANCEL_URL,
        )
        Order.objects.create(ebook=ebook, user=request.user)
        return redirect(checkout_session.url)


@login_required
def my_ebooks_view(request):
    orders = Order.objects.filter(user=request.user).order_by('created_at')
    return render(request, 'bought_ebooks.html', {'orders': orders})
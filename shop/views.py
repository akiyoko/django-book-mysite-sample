import logging

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import View

from .models import Book

logger = logging.getLogger(__name__)


class IndexView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        queryset = Book.objects.select_related('publisher').prefetch_related('authors').order_by('publish_date')
        keyword = request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(description__icontains=keyword)
            )
        context = {
            'keyword': keyword,
            'book_list': queryset,
        }
        return render(request, 'shop/book_list.html', context)


index = IndexView.as_view()


class DetailView(LoginRequiredMixin, View):
    def get(self, request, book_id, *args, **kwargs):
        book = Book.objects.get(pk=book_id)
        context = {
            'book': book,
            'stripe_pub_key': settings.STRIPE_PUBLISHABLE_KEY,
        }
        return render(request, 'shop/book_detail.html', context)


detail = DetailView.as_view()


class CheckoutView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        import time
        start_time = time.time()
        logger.info("User({}) posted the form.".format(request.user.id))

        stripe.api_key = settings.STRIPE_API_KEY
        token = request.POST['stripeToken']
        item_id = request.POST['item_id']
        book = get_object_or_404(Book, pk=item_id)

        try:
            charge = stripe.Charge.create(
                amount=book.price,
                currency='jpy',
                source=token,
                description=book.title,
            )
        except stripe.error.CardError as e:
            # The card has been declined
            return render(request, 'error.html', {
                'message': "Your payment cannot be completed. The card has been declined.",
            })

        logger.info("Charge[{}] created successfully.".format(charge.id))
        messages.info(request, "Your payment has been completed successfully.")
        logger.debug("Finished in {:.2f} secs.".format(time.time() - start_time))
        return render(request, 'shop/complete.html', {
            'charge': charge,
        })


checkout = CheckoutView.as_view()

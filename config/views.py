import logging

from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View

logger = logging.getLogger(__name__)


class IndexView(View):
    def get(self, request, *args, **kwargs):
        # return redirect(reverse('accounts:login'))
        return redirect('/accounts/login/')


index = IndexView.as_view()

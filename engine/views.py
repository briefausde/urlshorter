import json
import uuid
from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import *

from .models import *


class UserLinkRequiredMixin(LoginRequiredMixin):
    raise_exception = True

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not obj.user == request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class ShortUrlView(View):
    model = Url

    @staticmethod
    def generate_link():
        while True:
            short_url = uuid.uuid4().hex[:8]
            if not Url.objects.filter(short_url=short_url):
                return short_url

    def post(self, *args, **kwargs):
        link = self.request.POST.get('link', '')
        if link:
            short_url = self.generate_link()

            if self.request.user.is_authenticated:
                self.model.objects.create(user=self.request.user, original_url=link, short_url=short_url)
            else:
                self.model.objects.create(original_url=link, short_url=short_url)

            return HttpResponse('http://{}/{}'.format(self.request.get_host(), short_url))
        return HttpResponseBadRequest()


class RedirectUrlView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        url = get_object_or_404(Url, short_url=kwargs['url'])
        Click.objects.create(url=url)
        self.url = url.original_url
        return super().get_redirect_url(*args, **kwargs)


class UserLinksView(LoginRequiredMixin, ListView):
    model = Url
    context_object_name = 'urls'
    template_name = 'user_links_list.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).order_by('-pk')


class UserLinkDetailView(UserLinkRequiredMixin, DetailView):
    model = Url
    context_object_name = 'url'
    template_name = 'user_link_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['data_json'] = self.statistics()
        context['clicks'] = self.get_queryset()
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, short_url=self.kwargs['url'])

    def get_queryset(self):
        return Click.objects.filter(url__short_url=self.kwargs['url']).order_by('-pk')[:20]

    def statistics(self):
        data = {}
        date = timezone.now().date()
        for day in range(0, 31):
            count = Click.objects.filter(
                url__short_url=self.kwargs['url'],
                date__gte=date-timedelta(days=day),
                date__lte=date-timedelta(days=day-1)).count()
            data[(date-timedelta(days=day)).strftime("%d/%m")] = count
        return json.dumps(data)

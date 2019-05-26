from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic

from accounts.models import ProfileUser
from .models import FAQ
from .forms import AddFAQForm

# Create your views here.

def has_user_access_to_modify(current_user):

    if current_user.is_superuser:
        return True
    return False


def get_landing_page(request):
    # ('common/templates/landing-page.html')
    return render(request, 'landing-page.html')

#
# def get_faq_page(request):
#     # ('common/templates/landing-page.html')
#     return render(request, 'FAQ.html')


class AddFAQView(LoginRequiredMixin, generic.CreateView):
    model = FAQ
    form_class = AddFAQForm
    success_url = reverse_lazy('faq')
    template_name = 'add_faq_item.html'
    context_object_name = 'faq'


    def post(self, request, *args, **kwargs):
        form = AddFAQForm(request.POST)
        if not has_user_access_to_modify(self.request.user):
            return render(request, 'permission_denied.html')
        faq = form.save(commit=False)
        faq.question = form.cleaned_data['question']
        faq.answer = form.cleaned_data['answer']
        faq.save()
        return HttpResponseRedirect(reverse_lazy('faq'))


class AllFAQView(generic.ListView):
    model = FAQ
    template_name = 'FAQ.html'
    context_object_name = 'faqs'

    def get_queryset(self):
        offers = FAQ.objects.all()
        if offers:
            return offers
        return []
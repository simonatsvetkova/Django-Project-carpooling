from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic

from accounts.models import ProfileUser
from .models import FAQ
from .forms import AddFAQForm

# Create your views here.

def has_access_to_add_or_modify(current_user):

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
        if not has_access_to_add_or_modify(self.request.user):
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



class EditFAQView(LoginRequiredMixin, generic.CreateView):
    model = FAQ
    form_class = AddFAQForm
    success_url = reverse_lazy('faq')
    template_name = 'add_faq_item.html'
    context_object_name = 'faq'


    def get(self, request, pk):
        if has_access_to_add_or_modify(self.request.user):
            return render(request, 'add_faq_item.html', {'faqs': self.get_object()})
        return render(request, 'permission_denied.html')


    def post(self, request, *args, **kwargs):
        form = AddFAQForm(request.POST)
        if not has_access_to_add_or_modify(self.request.user):
            return render(request, 'permission_denied.html')
        faq = form.save(commit=False)
        faq.question = form.cleaned_data['question']
        faq.answer = form.cleaned_data['answer']
        faq.save()
        return HttpResponseRedirect(reverse_lazy('faq'))




class DeleteFAQView(LoginRequiredMixin, generic.DeleteView):
    model = FAQ
    login_url = 'accounts/login/'
    template_name = 'delete_faq_item.html'
    success_url = reverse_lazy('faq')

    def get(self, request, pk):
        if has_access_to_add_or_modify(self.request.user):
            return render(request, 'delete_faq_item.html', {'faqs': self.get_object()})
        return render(request, 'permission_denied.html')

    def post(self, request, pk):
        if not has_access_to_add_or_modify(self.request.user):
            return render(request, 'permission_denied.html')
        try:
            faq = FAQ.objects.get(pk=pk)
            faq.delete()
        except Exception as error:
            print(f"cant delete --> {error}")
        return HttpResponseRedirect(reverse_lazy('faq'))

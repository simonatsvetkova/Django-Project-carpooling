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


def get_faq_page(request):
    # ('common/templates/landing-page.html')
    return render(request, 'FAQ.html')


class AddFAQView(LoginRequiredMixin, generic.CreateView):
    model = FAQ
    form_class = AddFAQForm
    success_url = reverse_lazy('faq')
    template_name = 'FAQ.html'
    context_object_name = 'faq'
    #
    # def form_valid(self, request, form):
    #     if request.user.is_superuser:
    #         return super().form_valid(form)
    #     return render(request, 'permission_denied.html')
    #
    # def get(self, request):
    #     if has_user_access_to_modify(self.request.user):
    #         return render(request, 'add_faq_item.html', {'faq': self.get_object()})
    #     return render(request, 'permission_denied.html')
    #
    def post(self, request, *args, **kwargs):
        form = AddFAQForm(request.POST)
        if not has_user_access_to_modify(self.request.user):
            return render(request, 'permission_denied.html')
        faq = form.save(commit=False)
        faq.question = form.cleaned_data['question']
        faq.answer = form.cleaned_data['answer']
        faq.save()
        return HttpResponseRedirect(reverse_lazy('faq'))





# ***********************************
    #
    #
    # def post(self, request, *args, **kwargs):
    #     # if request.method == 'POST':
    #     form = AddFAQForm(request.POST)
    #     if form.is_valid():
    #         faq = form.save(commit=False)
    #         faq.question = form.cleaned_data['question']
    #         faq.answer = form.cleaned_data['answer']
    #         faq.save()
    #         return HttpResponseRedirect(reverse_lazy('faq'))
    #     return render(request, 'add_faq_item.html', {'form': form})
    #
    # #
    # def dispatch(self, request, *args, **kwargs):
    #     handler = super(AddFAQView, self).dispatch(request, *args, **kwargs)
    #     # Only allow editing if current user is admin
    #     if request.user.is_superuser:
    #         return handler
    #     return render(request, 'permission_denied.html')

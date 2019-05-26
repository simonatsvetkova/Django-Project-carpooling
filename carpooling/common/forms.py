from django import forms

from .models import FAQ


class AddFAQForm(forms.ModelForm):
    question = forms.CharField(max_length=255, required=True, widget=forms.Textarea(attrs={
                                         'class': 'form-control'
                                     }))

    answer = forms.CharField(max_length=1400, required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))

    class Meta:
        model = FAQ
        fields = ['question', 'answer']

    # def __init__(self, *args, **kwargs):
    #     super(AddFAQForm, self).__init__(*args, **kwargs)
    #
    #
    # def form_valid(self, form):
    #     obj = form.save(commit=False)
    #     obj.owner = self.request.user
    #     obj.save()
    #     return super().form_valid(form)
    #


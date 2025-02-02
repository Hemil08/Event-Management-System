from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Event,Category,Registration

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.USER_TYPES,required=True)

    class Meta:
        model = CustomUser
        fields = ['username','email','role','password1','password2']
        

class EventForm(forms.ModelForm):

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        empty_label="Select a Category",
        widget=forms.Select(attrs={'class':'form-control'})
        )

    start_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type':'datetime-local'}))
    end_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type':'datetime-local'}))

    class Meta:
        model = Event
        fields = [
            "title","photo","description","start_date","end_date","category","cost_per_person","available_slots"
        ]

        def clean_end_date(self):
            start_date = self.cleaned_data['start_date']
            end_date = self.cleaned_data['end_data']

            if end_date <= start_date:
                raise forms.ValidationError("End date must be later than start date")
            
            return end_date
        
class RegistrationForm(forms.ModelForm):

    class Meta:
        model = Registration
        fields = ["persons","contact_number"]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
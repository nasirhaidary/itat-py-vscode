from django import forms
from .models import Asset

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = '__all__'
        widgets = {
            'registration_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_ram(self):
        ram = self.cleaned_data.get('ram')
        if ram and ram < 0:
            raise forms.ValidationError("RAM cannot be negative")
        return ram

    def clean_storage(self):
        storage = self.cleaned_data.get('storage')
        if storage and storage < 0:
            raise forms.ValidationError("Storage cannot be negative")
        return storage
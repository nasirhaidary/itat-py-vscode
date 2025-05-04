from django import forms
from .models import Asset

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = '__all__'
        widgets = {
            'registration_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'asset_id': forms.TextInput(attrs={
                'readonly': 'readonly',
                'class': 'form-control-plaintext',
                'placeholder': 'Will be auto-generated'
            }),
            'asset_type': forms.Select(attrs={'class': 'form-select'}),
            'operating_system': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
            'processor': forms.TextInput(attrs={'required': False}),
            'ram': forms.NumberInput(attrs={'required': False}),
            'storage': forms.NumberInput(attrs={'required': False}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:  # If this is a new asset
            self.fields['asset_id'].required = False  # Don't require asset_id for new assets
        
        # Make processor, RAM, and storage optional
        self.fields['processor'].required = False
        self.fields['ram'].required = False
        self.fields['storage'].required = False

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
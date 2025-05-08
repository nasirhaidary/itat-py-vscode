from django import forms
from .models import Asset, AssetCheckout, AssetMovement

class AssetForm(forms.ModelForm):
    asset_type = forms.ChoiceField(
        choices=[('', 'Select asset type')] + list(Asset.ASSET_TYPE_CHOICES),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    operating_system = forms.ChoiceField(
        choices=[('', 'Choose operating system')] + list(Asset.OS_CHOICES),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    status = forms.ChoiceField(
        choices=[('', 'Select status')] + list(Asset.STATUS_CHOICES),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    condition = forms.ChoiceField(
        choices=[('', 'Select condition')] + list(Asset.CONDITION_CHOICES),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    ram_unit = forms.ChoiceField(
        choices=Asset.UNIT_CHOICES,
        initial='GB',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    storage_unit = forms.ChoiceField(
        choices=Asset.UNIT_CHOICES,
        initial='GB',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Asset
        fields = '__all__'
        widgets = {
            'registration_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'asset_id': forms.TextInput(attrs={
                'readonly': 'readonly',
                'class': 'form-control',
                'style': 'background-color: #f8f9fa;'
            }),
            'processor': forms.TextInput(attrs={'required': False}),
            'ram': forms.NumberInput(attrs={
                'required': False,
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Enter size'
            }),
            'storage': forms.NumberInput(attrs={
                'required': False,
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Enter size'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:  # If this is a new asset
            self.fields['asset_id'].required = False
            
            # Generate the next asset ID
            last_asset = Asset.objects.order_by('-asset_id').first()
            if last_asset and last_asset.asset_id.startswith('BDAsset-'):
                last_number = int(last_asset.asset_id.split('-')[1])
                new_number = last_number + 1
            else:
                new_number = 1
            next_asset_id = f'BDAsset-{new_number:03d}'
            
            # Set the initial value for the asset_id field
            self.fields['asset_id'].initial = next_asset_id
        
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

class AssetCheckoutForm(forms.ModelForm):
    class Meta:
        model = AssetCheckout
        fields = ['expected_return_date', 'notes']
        widgets = {
            'expected_return_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'notes': forms.Textarea(
                attrs={'rows': 3, 'class': 'form-control'}
            ),
        }

class AssetMovementForm(forms.ModelForm):
    class Meta:
        model = AssetMovement
        fields = ['to_location', 'reason']
        widgets = {
            'to_location': forms.TextInput(attrs={'class': 'form-control'}),
            'reason': forms.Textarea(
                attrs={'rows': 3, 'class': 'form-control'}
            ),
        }
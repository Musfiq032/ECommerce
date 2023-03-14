from django import forms

PAYMENT_CHOICE= {
    ('C','Cash on Delivery'),
    ('O', 'Online Payment')
}
class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'class' : "form-control",
        'placeholder': 'House number and Street name',
        'id': 'address'
    }))
    email_address = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': "form-control",
        'placeholder': 'Email Address',
        'id': 'email'
    }))

    mobile_no= forms.IntegerField(widget=forms.TextInput(attrs={
        'class': "form-control",
        'placeholder': 'Mobile No.',
        'id': 'mobile_no'
    }))
    payment_option= forms.ChoiceField( widget=forms.RadioSelect, choices=PAYMENT_CHOICE)
    notes = forms.TimeField(widget=forms.TextInput(attrs={
        'class': "form-control",
        'placeholder': 'Notes about your order, e.g. special notes for delivery',
        'id': 'notes'
    }))
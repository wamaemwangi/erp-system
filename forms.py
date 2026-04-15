from django import forms
from .models import PettyCash, Imprest, SalaryAdvance, ImprestSurrender


# ----------------------------
# PETTY CASH FORM (FIXED - NO document field)
# ----------------------------
class PettyCashForm(forms.ModelForm):
    # Override these fields to be optional because they are supplied via the items table
    amount = forms.DecimalField(required=False, max_digits=10, decimal_places=2)
    description = forms.CharField(required=False, widget=forms.Textarea)

    class Meta:
        model = PettyCash
        fields = [
            'amount',
            'from_date',
            'to_date',
            'description',
            'department',
        ]
        widgets = {
            'from_date': forms.DateInput(attrs={'type': 'date'}),
            'to_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        # Only validate if an amount was provided (skip when using items)
        if amount is not None and amount > 3000:
            raise forms.ValidationError("Amount cannot exceed 3000")
        return amount


# ----------------------------
# IMPREST FORM
# ----------------------------
class ImprestForm(forms.ModelForm):
    # Override these fields to be optional
    amount = forms.DecimalField(required=False, max_digits=10, decimal_places=2)
    description = forms.CharField(required=False, widget=forms.Textarea)

    class Meta:
        model = Imprest
        fields = [
            'amount',
            'description',
            'from_date',
            'to_date',
            'department',
            'document'
        ]
        widgets = {
            'from_date': forms.DateInput(attrs={'type': 'date'}),
            'to_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        # Skip validation if no amount (will be set from items)
        if amount is not None and amount <= 3000:
            raise forms.ValidationError("Imprest must be above 3,000.")
        return amount


# ----------------------------
# SALARY ADVANCE FORM
# ----------------------------
class SalaryAdvanceForm(forms.ModelForm):
    class Meta:
        model = SalaryAdvance
        fields = ['amount', 'purpose']


# ----------------------------
# IMPREST SURRENDER FORM
# ----------------------------
class ImprestSurrenderForm(forms.ModelForm):
    class Meta:
        model = ImprestSurrender
        fields = ['imprest', 'amount_spent', 'balance_returned']


# ----------------------------
# PETTY CASH REJECT FORM
# ----------------------------
class PettyCashRejectForm(forms.ModelForm):
    class Meta:
        model = PettyCash
        fields = ['status', 'description']
        widgets = {
            'status': forms.HiddenInput(),
            'description': forms.Textarea(attrs={
                'placeholder': 'Reason for rejection (optional)',
                'rows': 2
            }),
        }
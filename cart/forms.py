from django import forms
from .models import Form


class OrderForm(forms.ModelForm):

    class Meta:
        model = Form
        exclude = ('created_at',)
        widgets = {
            'name': forms.TextInput(attrs={'placeholder':'フルネームで入力'}),
            'address': forms.TextInput(attrs={'placeholder':'続きから入力'}),
            'tel': forms.TextInput(attrs={'placeholder':'半角数字ハイフンなし','pattern':'^[0-9]+$'}),
            'text': forms.Textarea(attrs={'placeholder':'辛さの指定やアレルギーなどがある方はこちらにご記入ください。','class':'textarea'}),
        }

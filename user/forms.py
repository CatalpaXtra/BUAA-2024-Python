from django import forms
from django.contrib.auth import get_user_model
from .models import CaptchaModel

User = get_user_model()


class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    captcha = forms.CharField(max_length=4, min_length=4)
    password = forms.CharField()

    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha')
        email = self.cleaned_data.get('email')

        captcha_model = CaptchaModel.objects.filter(email=email, captcha=captcha).first()
        if not captcha_model:
            raise forms.ValidationError("验证码和邮箱不匹配！")
        captcha_model.delete()
        return captcha


class ResetForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()
    captcha = forms.CharField(max_length=4, min_length=4)


class ModifyForm(forms.Form):
    username = forms.CharField()
    gender = forms.CharField(max_length=16)
    age = forms.IntegerField()
    height = forms.IntegerField()
    weight = forms.FloatField()
    

class ModifyPasswordForm(forms.Form):
    password = forms.CharField()
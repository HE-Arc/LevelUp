from django import forms
from django.contrib.auth.models import User

class CreateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("Un utilisateur avec cet email existe déjà.")
        return email

    def save(self, commit=True) -> User:
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]  # Utilisation de l'email comme username
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
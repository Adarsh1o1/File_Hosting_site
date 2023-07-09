from django import forms
from .models import files
from django.forms import ClearableFileInput

# class file_upload(forms.ModelForm):
#     file= MultiFileField(min_num=1, max_num=10, max_file_size=1024*1024*5, widget=forms.ClearableFileInput(attrs={'multiple': True}))

#     class Meta:
#         model = files
#         fields = ["file"]
#         # widgets = {
#         #     'file': MultiFileField(min_num=1, max_num=10, max_file_size=1024*1024*5, widget=forms.ClearableFileInput(attrs={'multiple': True})),
#         # }
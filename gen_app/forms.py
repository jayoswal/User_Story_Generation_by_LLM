# forms.py
from django import forms

class TextInputForm(forms.Form):
    inp_prompt = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'id':'yest-iddd', 'maxlength':'16384'}),
        label='Enter Software Requirement Text',
        required=False
    )
    file_input = forms.FileField(
        label='Upload a Text File',
        help_text='Only .txt files are allowed.',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file', 'id':'file_upload'}),
        required=False
    )



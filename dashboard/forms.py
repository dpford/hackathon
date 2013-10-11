from django import forms

class BoardsForm(forms.ModelForm):
    # dot his dynamically http://jacobian.org/writing/dynamic-form-generation/

    class Meta:
        model = ExcelloUser
from django import forms
from . import models


class insertform(forms.ModelForm):
    class Meta:
        model = models.Booktime
        fields = "__all__"
        widgets = {'CoachName': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(insertform, self).__init__(*args, **kwargs)
        self.fields['Slotperiodfrom'] = forms.ChoiceField()

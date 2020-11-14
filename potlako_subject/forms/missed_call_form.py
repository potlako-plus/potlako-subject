from django import forms

from ..models import MissedCall, MissedCallRecord
from .form_mixins import SubjectModelFormMixin


class MissedCallForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = MissedCall
        fields = '__all__'
        
class MissedCallRecordForm(forms.ModelForm):
    
    

    class Meta:
        model = MissedCallRecord
        fields = '__all__'

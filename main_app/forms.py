from django.forms import ModelForm, Textarea
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from crispy_forms.bootstrap import FormActions

from .models import MyModel

class MyForm(ModelForm): 

    def __init__(self, *args, **kwargs):
        super(MyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.layout = Layout( 
            FormActions(Submit('BlahBlah', 'BlahBlah', css_class='btn-primary')))

    class Meta:
        model = MyModel
        fields = ['xxx', 'yyy']
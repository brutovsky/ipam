from django.forms.widgets import Input
from django.db import models

class ColorField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10
        super(ColorField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = ColorWidget
        return super(ColorField, self).formfield(**kwargs)

class ColorWidget(Input):
    input_type = 'color'
    template_name = 'django/forms/widgets/text.html'

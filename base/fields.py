from django import forms

class BooleanChoiceField(forms.NullBooleanField):
    def __init__(self,*args,**kwargs):
        super(BooleanChoiceField,self).__init__(*args,**kwargs)
        self.widget.choices = ((1, "------"), (2,"Yes"), (3, "No"))


    def clean(self, value):
        val = super(BooleanChoiceField, self).clean(value)

        if val is None:
            raise forms.ValidationError("This field is required.")

        return val
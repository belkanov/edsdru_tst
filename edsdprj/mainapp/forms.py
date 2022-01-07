from django import forms


class AnswerForm(forms.Form):
    user_answer = forms.IntegerField(min_value=10, max_value=99, label='Ваше загаданное число')

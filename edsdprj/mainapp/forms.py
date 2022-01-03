from django import forms


class MainForm(forms.Form):
    user_answer = forms.IntegerField(min_value=10, max_value=99, label='Введите число от 10 до 99')

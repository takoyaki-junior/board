from django import forms
from .models import Topic


class WriteForm(forms.ModelForm):
    class Meta:
        # モデルを指定
        model = Topic
        # フォームとして表示したいカラムを指定
        fields = ('text',)

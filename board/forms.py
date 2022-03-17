from django.forms import ModelForm
from .models import Thread, Comment


class ThreadForm(ModelForm):
    class Meta:
        # モデルを指定
        model = Thread
        # フォームとして表示したいカラムを指定
        fields = ("title", "content")


class CommentForm(ModelForm):
    class Meta:
        # モデルを指定
        model = Comment
        # フォームとして表示したいカラムを指定
        fields = ("comment",)

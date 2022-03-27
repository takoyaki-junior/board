from django.forms import ModelForm
from .models import Thread, Comment


class ThreadForm(ModelForm):
    class Meta:
        # モデルを指定
        model = Thread
        # フォームとして表示したいカラムを指定
        fields = [
            'title',
            'category',
            'content',
        ]

        def __init__(self, *args, **kwargs):
            # kwargs.setdefault('label_suffix', '')
            super().__init__(*args, **kwargs)
            # self.fields['title'].widget.attrs['class'] = 'huga'
            self.fields['category'].empty_label = '選択して下さい'
            # self.fields['user_name'].widget.attrs['value'] = '匿名'


class CommentForm(ModelForm):
    class Meta:
        # モデルを指定
        model = Comment
        # フォームとして表示したいカラムを指定
        fields = ("comment",)

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        # self.fields['user_name'].widget.attrs['value'] = '名無し'

    def save_with_thread(self, id, user, commit=True):
        comment = self.save(commit=False)
        # threadにログイン中ユーザー情報を追加
        comment.thread = Thread.objects.get(id=id)
        comment.no = Comment.objects.filter(id=id).count() + 1
        comment.created_by = user
        if commit:
            comment.save()
        return comment

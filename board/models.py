from django.db import models
from accounts.models import User


class Thread(models.Model):

    # カラム
    title = models.CharField(
        verbose_name='タイトル', blank=False, null=False, max_length=150)
    content = models.TextField(
        verbose_name='内容', blank=True, null=True)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(
        verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(
        verbose_name='更新日時', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'thread'


class Comment(models.Model):

    # カラム
    comment = models.TextField(
        verbose_name='コメント', blank=False, null=False)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT)
    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE)
    created_at = models.DateTimeField(
        verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(
        verbose_name='更新日時', auto_now=True)

    def __str__(self):
        return self.message

    class Meta:
        db_table = 'comment'

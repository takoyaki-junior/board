from django.db import models
from django.utils import timezone


class Topic(models.Model):

    # カラム名=データの形式(管理画面に表示される名前,その他の制約)
    text = models.CharField(verbose_name='本文', max_length=255)
    created_at = models.DateField(verbose_name='作成日', default=timezone.now)

    # 管理画面に表示されるように設定(おまじない)
    def __str__(self):
        return self.text, self.created_at

    # Metaとかobjectとかはおまじない
    class Meta:
        db_table = 'topic'

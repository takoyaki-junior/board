from django.db import models
from accounts.models import User

# トピックのステータス一覧
TOPIC_STATUS_CHOICE = (
    (0, '公開'),
    (1, '非公開'),
    (2, '承認待ち'),
)

# トピックのステータス一覧
COMMENT_STATUS_CHOICE = (
    (0, '公開'),
    (1, '非公開'),
)


class ThreadManager(models.Manager):
    # Thread操作に関する処理を追加
    pass


class CommentManager(models.Manager):
    # Comment操作に関する処理を追加
    pass


class CategoryManager(models.Manager):
    # Category操作に関する処理を追加
    pass


class Category(models.Model):
    name = models.CharField(
        'カテゴリー名',
        max_length=50,
    )
    url_code = models.CharField(
        'URLコード',
        max_length=50,
        null=True,
        blank=False,
        unique=True,
    )
    sort = models.IntegerField(
        verbose_name='ソート',
        default=0,
    )
    objects = CategoryManager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'


class Thread(models.Model):

    # カラム
    title = models.CharField(
        verbose_name='タイトル', blank=False, null=False, max_length=150)
    content = models.TextField(
        verbose_name='内容', blank=True, null=True)
    created_by = models.ForeignKey(
        User, verbose_name='投稿者', on_delete=models.PROTECT)
    category = models.ForeignKey(
        Category,  verbose_name='カテゴリー', on_delete=models.PROTECT, null=True, blank=False)
    status = models.IntegerField(
        verbose_name='トピックのステータス', default=0, choices=TOPIC_STATUS_CHOICE)
    created_at = models.DateTimeField(
        verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(
        verbose_name='更新日時', auto_now=True)

    objects = ThreadManager()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'thread'


class Comment(models.Model):

    # カラム
    id = models.BigAutoField(
        primary_key=True)
    no = models.IntegerField(default=0)
    comment = models.TextField(
        verbose_name='コメント', blank=False, null=False)
    created_by = models.ForeignKey(
        User, verbose_name='投稿者', on_delete=models.PROTECT)
    thread = models.ForeignKey(
        Thread, verbose_name='スレッド', on_delete=models.CASCADE)
    status = models.IntegerField(
        verbose_name='コメントのステータス', default=0, choices=COMMENT_STATUS_CHOICE)
    created_at = models.DateTimeField(
        verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(
        verbose_name='更新日時', auto_now=True)

    objects = CommentManager()

    def __str__(self):
        return self.message

    class Meta:
        db_table = 'comment'

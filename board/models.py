from django.db import models
from accounts.models import User
from django.core.validators import FileExtensionValidator

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
    def create_comment(self, created_by, comment, thread_id, image=None):
        comment = self.model(
            created_by=created_by,
            comment=comment,
            image=image
        )
        comment.thread = Thread.objects.get(id=thread_id)
        comment.no = self.filter(thread_id=thread_id).count() + 1
        comment.save()


class CategoryManager(models.Manager):
    # Category操作に関する処理を追加
    pass


class VoteManager(models.Manager):
    def create_vote(self, ip_address, comment_id):
        vote = self.model(
            ip_address=ip_address,
            comment_id=comment_id
        )
        try:
            vote.save()
        except:
            return False
        return True


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
    image = models.ImageField(
        verbose_name='投稿画像',
        validators=[FileExtensionValidator(['jpg', 'png'])],
        upload_to='images/%Y/%m/%d/', null=True, blank=True,
    )
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


class Vote(models.Model):
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        null=True,
    )
    ip_address = models.CharField(
        'IPアドレス',
        max_length=50,
    )

    objects = VoteManager()

    def __str__(self):
        return '{}-{}'.format(self.comment.topic.title, self.comment.no)

    class Meta:
        db_table = 'vote'

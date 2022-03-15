from django.shortcuts import render, redirect
from django.views import View
from .models import Topic
from .forms import CreateForm
import logging


class BoardView(View):

    def get(self, request, *args, **kwargs):

        queryset = Topic.objects.all().order_by('-created_at')
        # ログ出力
        logger = logging.getLogger(__name__)
        logger.info("テスト用info")

        return render(request, "board/index.html", {'topics': queryset})


index = BoardView.as_view()


class CreateView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'board/create.html', {'form': CreateForm})

    def post(self, request, *args, **kwargs):
        # formに書いた内容を格納する
        form = CreateForm(request.POST)
        # 保存する前に一旦取り出す
        post = form.save(commit=False)
        # 保存
        post.save()
        # ログ出力
        logger = logging.getLogger(__name__)
        logger.info("テスト用info")
        # indexのviewに移動
        return redirect(to='board:index')


create = CreateView.as_view()

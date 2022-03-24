from django.shortcuts import render, redirect
from django.views import View, generic
from .models import Thread, Comment
from .forms import ThreadForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
import logging
from django.urls import reverse_lazy
from django.http import HttpResponse


class BoardListView(LoginRequiredMixin, generic.ListView):
    template_name = 'board/index.html'
    queryset = Thread.objects.all().order_by('-created_at')
    context_object_name = 'threads'
    # ログ出力
    logger = logging.getLogger(__name__)
    logger.info("スレッドを表示")


index = BoardListView.as_view()


class BoardDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'board/detail.html'
    model = Thread
    context_object_name = 'threads'
    # ログ出力
    logger = logging.getLogger(__name__)
    logger.info("一覧コメントを表示")


detail = BoardDetailView.as_view()


class BoardCreateView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'board/create.html', {'form': ThreadForm})

    def post(self, request, *args, **kwargs):
        # formに書いた内容を格納する
        form = ThreadForm(request.POST)
        if form.is_valid():
            # DBに登録する準備を行う
            thread = form.save(commit=False)
            # threadにログイン中ユーザー情報を追加
            thread.created_by = request.user
            # 保存
            thread.save()
            # ログ出力
            logger = logging.getLogger(__name__)
            logger.info("スレッドを作成しました")

        # indexのviewに移動
        return redirect(to='board:index')


create = BoardCreateView.as_view()


class BoardUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    template_name = 'board/update.html'
    model = Thread
    fields = ['content', 'title', ]

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if obj.created_by.id != self.request.user.id:
            raise PermissionDenied('You do not have permission to edit.')

        return super(BoardUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('board:index')

    def get_form(self):
        form = super(BoardUpdateView, self).get_form()
        form.fields['title'].label = 'タイトル'
        form.fields['content'].label = '内容'
        return form


update = BoardUpdateView.as_view()


class DeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    template_name = 'board/delete.html'
    model = Thread
    success_url = reverse_lazy('board:index')


delete = DeleteView.as_view()

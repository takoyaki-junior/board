from django.shortcuts import get_object_or_404, render, redirect
from django.views import View, generic
from .models import Category, Thread, Comment
from .forms import ThreadForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Count
import logging
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.core.mail import send_mail, EmailMessage
from django.template.loader import get_template


class BoardListView(LoginRequiredMixin, generic.ListView):
    template_name = 'board/index.html'
    queryset = Thread.objects.all().order_by('-created_at')
    context_object_name = 'threads'
    # ログ出力
    logger = logging.getLogger(__name__)
    logger.info("スレッドを表示")


index = BoardListView.as_view()


class CategoryView(LoginRequiredMixin, generic.ListView):
    template_name = 'board/category.html'
    context_object_name = 'threads'
    paginate_by = 1  # 1ページに表示するオブジェクト数 サンプルのため1にしています
    page_kwarg = 'p'  # GETでページ数を受けるパラメータ名。指定しないと'page'がデフォルト

    def get_queryset(self):
        return Thread.objects.filter(category__url_code=self.kwargs['url_code'])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['category'] = get_object_or_404(
            Category, url_code=self.kwargs['url_code'])
        return ctx


class BoardDetailView(LoginRequiredMixin, generic.FormView):
    template_name = 'board/detail.html'
    form_class = CommentForm

    def form_valid(self, form):
        # comment = form.save(commit=False)  # 保存せずオブジェクト生成する
        # comment.thread = Thread.objects.get(id=self.kwargs['pk'])
        # comment.no = Comment.objects.filter(
        #     thread=self.kwargs['pk']).count() + 1
        # comment.created_by = self.request.user
        # comment.save()
        # コメント保存のためsave_with_threadメソッドを呼ぶ
        Comment.objects.create_comment(
            created_by=self.request.user,
            comment=form.cleaned_data['comment'],
            thread_id=self.kwargs['pk'],
            image=form.cleaned_data['image']
        )
        form.save_with_thread(self.kwargs.get('pk'), self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('board:detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self):
        ctx = super().get_context_data()
        ctx['thread'] = Thread.objects.get(id=self.kwargs['pk'])
        ctx['comments'] = Comment.objects.filter(
            thread=self.kwargs['pk']).annotate(vote_count=Count('vote')).order_by('no')
        return ctx


detail = BoardDetailView.as_view()


# class BoardCreateView(LoginRequiredMixin, generic.CreateView):
#     template_name = 'board/create.html'
#     form_class = ThreadForm
#     model = Thread
#     success_url = reverse_lazy('board:index')

#     def form_valid(self, form):
#         ctx = {'form': form}
#         if self.request.POST.get('next', '') == 'confirm':
#             return render(self.request, 'board/create_confirm.html', ctx)
#         if self.request.POST.get('next', '') == 'back':
#             return render(self.request, 'board/create.html', ctx)
#         if self.request.POST.get('next', '') == 'create':
#             # DBに登録する準備を行う
#             thread = form.save(commit=False)
#             # threadにログイン中ユーザー情報を追加
#             thread.created_by = self.request.user
#             # 保存
#             thread.save()
#             # ログ出力
#             logger = logging.getLogger(__name__)
#             logger.info("スレッドを作成しました")
#             # メール送信処理
#             template = get_template('board/mail/board_mail.html')
#             mail_ctx = {
#                 'title': form.cleaned_data['title'],
#                 'created_by': self.request.user,
#                 'content': form.cleaned_data['content'],
#             }
#             # EmailMessage(
#             #     subject='トピック作成: ' + form.creaned_data['title'],
#             #     body=template.render(mail_ctx),
#             #     from_email='test@example.com',
#             #     to=['admin2@example.com'],
#             #     # cc=['admin2@example.com'],
#             #     # bcc=['admin3@example.com'],
#             # ).send()
#             return super().form_valid(form)
#         else:
#             # 正常動作ではここは通らない。エラーページへの遷移でも良い
#             return redirect(reverse_lazy('board:index'))


# create2 = BoardCreateView.as_view()


class BoardCreateViewBySession(LoginRequiredMixin, generic.FormView):
    template_name = 'board/create.html'
    form_class = ThreadForm

    def post(self, request, *args, **kwargs):
        ctx = {}
        if request.POST.get('next', '') == 'back':
            if 'input_data' in self.request.session:
                input_data = self.request.session['input_data']
                form = ThreadForm(input_data)
                ctx['form'] = form
            return render(request, self.template_name, ctx)

        elif request.POST.get('next', '') == 'create':
            if 'input_data' in request.session:
                form = self.form_class(request.session['input_data'])
                # DBに登録する準備を行う
                thread = form.save(commit=False)
                # threadにログイン中ユーザー情報を追加
                thread.created_by = self.request.user
                # 保存
                thread.save()
                # ログ出力
                logger = logging.getLogger(__name__)
                logger.info("スレッドを作成しました2")
                # メール送信処理は省略

                response = redirect(reverse_lazy('board:index'))
                response.set_cookie(
                    'categ_id', request.session['input_data']['category'])
                request.session.pop('input_data')  # セッションに保管した情報の削除
                return response

        elif request.POST.get('next', '') == 'confirm':
            form = ThreadForm(request.POST)
            if form.is_valid():
                ctx = {'form': form}
                # セッションにデータを保存
                input_data = {
                    'title': form.cleaned_data['title'],
                    'content': form.cleaned_data['content'],
                    'category': form.cleaned_data['category'].id,
                }
                request.session['input_data'] = input_data
                ctx['category'] = form.cleaned_data['category']
                return render(request, 'board/create_confirm.html', ctx)
            else:
                return render(request, self.template_name, {'form': form})

    def get_context_data(self):
        ctx = super().get_context_data()
        if 'categ_id' in self.request.COOKIES:
            form = ctx['form']
            form['category'].field.initial = self.request.COOKIES['categ_id']
            ctx['form'] = form
        return ctx


create = BoardCreateViewBySession.as_view()


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

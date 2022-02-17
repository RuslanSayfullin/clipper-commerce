from django.core import paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .forms import EmailPostForm
from .models import Post


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_share(request, post_id):
    # Получение статьи по идентификатору.
    post = get_object_or_404(Post, id=post_id, status='published')
    if request.method == 'POST':
        # Форма была отправлена на сохранение.
        form = EmailPostForm(request.POST)
        if form.is_valid():     # Все поля формы прошли валидацию.
            cd = form.cleaned_data
            # ... Отправка электронной почты.
        else:
            form = EmailPostForm()
            return render(request, 'blog/post/share.html',
                          {'post': post, 'form': form})


# def post_list(request):
#     object_list = Post.published.all()
#     paginator = Paginator(object_list, 3)   # 3 статьи на каждой странице
#     page = paginator.Get.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         "Если страница не является целым числом, возвращаем первую страницу."
#         posts = paginator.page(1)
#     except EmptyPage:
#         #   Если номер страницы больше, чем общее количество страниц, возвращаем последнюю.
#         posts = paginator.page(paginator.num_pages)
#     return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year,
                             publish__month=month, publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})
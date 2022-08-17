from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone

from .foms import PostForm
from .models import Post


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by(
        "published_date"
    )
    return render(request, "blog/post_list.html", {"posts": posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "blog/post_detail.html", {"post": post})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "GET":
        form = PostForm(instance=post)
        return render(request, "blog/post_edit.html", {"form": form})

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)  # POSTデータを変数formに保存
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect("post_detail", pk=post.pk)


def post_new(request):
    if request.method == "GET":
        form = PostForm()
        return render(request, "blog/post_edit.html", {"form": form})

    if request.method == "POST":
        form = PostForm(request.POST)  # POSTデータを変数formに保存
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect("post_detail", pk=post.pk)

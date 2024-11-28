from django.views import generic
from django.shortcuts import get_object_or_404, render
from .models import Post, Comment
from .forms import CommentForm

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')  # Filter for published posts
    template_name = 'index.html'  # Template to render the list of posts


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)  # Get the post by slug or return a 404
    comments = post.comments.filter(active=True)  # Filter for active comments
    new_comment = None

    if request.method == 'POST':
        # Process the submitted comment form
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create a new comment instance without saving it to the database yet
            new_comment = comment_form.save(commit=False)
            new_comment.post = post  # Associate the comment with the current post
            new_comment.save()
    else:
        comment_form = CommentForm()  # Render an empty form for a GET request

    # Render the template with the post and its related data
    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
    })

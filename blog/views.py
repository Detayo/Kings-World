from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm, ContactForm
from django.contrib.auth.decorators import login_required
from django.core.mail import BadHeaderError, send_mail
from django.conf import settings

	
	
def home(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
	paginator = Paginator(posts, 10)
	page = request.GET.get('page')
	post=paginator.get_page(page)
	return render(request, 'blog/home.html', {'posts': posts})
	

	
def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post': post})
	
@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
   
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)
    

@login_required    
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

def about(request):
	return render(request,'blog/about.html',{'title':'about'})
	
def contact(request):
	if request.method == 'GET':
		form = ContactForm()
		
	else:
		form = ContactForm(request.POST)
		if form.is_valid():
			subject = form.cleaned_data['subject']
			from_email = form.cleaned_data['Email']
			message = form.cleaned_data['message']
			try:
				send_mail(subject, message, from_email, ['adetayolanipekun@gmail.com'])
			except BadHeaderError:
				return HttpResponse('Invalid header found.')
			return redirect('success')
	return render(request, "blog/contact.html", {'form': form})

def successView(request):
    return HttpResponse('Sent! DetayoKing will reply soonest, thanks')

		

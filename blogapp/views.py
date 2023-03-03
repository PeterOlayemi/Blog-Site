from .models import BlogModel,CommentModel, User
from .forms import SearchForm,CommentForm, PostForm, RegisterForm, LoginForm
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, logout, login
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# General

def index(request):
    return render(request, 'index.html')

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                if user.is_admin:
                    login(request, user)
                    return redirect('adminblogs')
                elif user.is_writer:
                    login(request, user)
                    return redirect('writerblogs')
                elif user.is_reader:
                    login(request, user)
                    return redirect('readerblogs')
                else:
                    msg= 'invalid credentials'
            else:
                msg= 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'login.html', {'form': form, 'msg': msg})

@login_required
def signout(request):
    logout(request)
    return redirect('index')

# Admin Views

@login_required
def admineditpost(request, _id):
    post = BlogModel.objects.get(id=_id)
    if request.method != 'POST':
        form = PostForm(instance=post)
    else:
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminblog', args=[post.id]))
    context = {'post': post, 'form': form}
    return render(request, 'admineditpost.html', context)

@login_required
def admindeletepost(request, _id):
    deletepost=BlogModel.objects.get(id=_id)
    blog=deletepost.blog
    deletepost.delete()
    return HttpResponseRedirect(reverse('adminblogs'))

@login_required
def AdminBlogDetailView(request, _id):
    try:
        data =BlogModel.objects.get(id =_id)
        comments = CommentModel.objects.filter(blog = data).order_by('-date_added')
    except BlogModel.DoesNotExist:
        raise Http404('Data does not exist')
     
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment=form.save(commit=False)
            Comment.blog=data
            Comment.owned=request.user
            Comment.save()
            return redirect(f'/adminblog/{_id}')
    else:
        form = CommentForm()
 
    context = {
            'data':data,
            'form':form,
            'comments':comments
        }
    return render(request,'admindetailview.html',context)

def adminregister(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        admin = form.save(commit=False)
        admin.is_admin == True
        admin.save()
        return redirect('login_view')
    return render(request,'adminregister.html', {'form': form})

def writerregister(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        writer = form.save(commit=False)
        writer.is_writer == True
        writer.save()
        return redirect('login_view')
    return render(request,'writerregister.html', {'form': form})

def readerregister(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        reader = form.save(commit=False)
        reader.is_reader == True
        reader.save()
        return redirect('login_view')
    return render(request,'readerregister.html', {'form': form})

@login_required
def adminate(request, _id):
    user = User.objects.get(id=_id)
    user.is_admin=True
    user.is_writer=False
    user.is_reader=False
    user.save()
    return redirect('user')

@login_required
def user(request):
    user = User.objects.filter(is_admin=False).order_by('-date_joined')
    context = {
            'user': user
        }
    return render(request, 'user.html', context)

@login_required
def deleteuser(request, _id):
    use = User.objects.get(id=_id)
    use.delete()
    return HttpResponseRedirect(reverse('user'))
 
@login_required
def AdminBlogListView(request):
    dataset = BlogModel.objects.all().order_by('-date_added')
    paginator = Paginator(dataset, 5)
    page = request.GET.get('page')
    try:
        dataset = paginator.page(page)
    except PageNotAnInteger:
        dataset = paginator.page(1)
    except EmptyPage:
        dataset = paginator.page(paginator.num_pages)
    try:
        if request.method == 'POST':
            form = SearchForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                blog = BlogModel.objects.get(blog_title=title)
                return redirect(f'/adminblog/{blog.id}')
    except BlogModel.DoesNotExist:
        raise Http404
    else:
        form = SearchForm()
        context = {
            'dataset':dataset,
            'form':form,
            'page': page,
        }
        return render(request, 'adminlistview.html', context)

@login_required
def admineditcomment(request, _id):
    comment = CommentModel.objects.get(id=_id)
    blog=comment.blog
    if request.method != 'POST':
        form = CommentForm(instance=comment)
    else:
        form = CommentForm(instance=comment, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminblog', args=[blog.id]))
    context = {'comment': comment, 'form': form}
    return render(request, 'admineditcomment.html', context)

@login_required
def admindeletecomment(request, _id):
    deleter=CommentModel.objects.get(id=_id)
    blog=deleter.blog
    deleter.delete()
    return HttpResponseRedirect(reverse('adminblog', args=[blog.id]))

@login_required
def adminaboutus(request):
    return render(request, 'adminaboutus.html')

@login_required
def admincontactus(request):
    return render(request, 'admincontactus.html')

@login_required
def adminaddpost(request):
    if request.method != 'POST':
        form = PostForm() 
    else:
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = request.user
            new_post.save()
            return HttpResponseRedirect(reverse('adminblogs'))
    context = {'form': form}
    return render(request, 'adminaddpost.html', context)

# Writer Views

@login_required
def WriterBlogListView(request):
    dataset = BlogModel.objects.all().order_by('-date_added')
    paginator = Paginator(dataset, 5)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        dataset = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        dataset = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        dataset = paginator.page(paginator.num_pages)
    try:
        if request.method == 'POST':
            form = SearchForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                blog = BlogModel.objects.get(blog_title=title)
                return redirect(f'/writerblog/{blog.id}')
    except BlogModel.DoesNotExist:
        raise Http404
    else:
        form = SearchForm()
        context = {
            'dataset':dataset,
            'form':form,
            'page': page,
        }
        return render(request,'writerlistview.html', context) 

def writerregister(request):
    msg = None
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_writer=True
            user.save()
            msg = 'user created'
            return redirect('login_view')
        else:
            msg = 'form is not valid'
    else:
        form = RegisterForm()
    return render(request,'writerregister.html', {'form': form, 'msg': msg})

@login_required
def WriterBlogDetailView(request,_id):
    try:
        data =BlogModel.objects.get(id =_id)
        comments = CommentModel.objects.filter(blog = data).order_by('-date_added')
    except BlogModel.DoesNotExist:
        raise Http404('Data does not exist')
     
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment=form.save(commit=False)
            Comment.blog=data
            Comment.owned=request.user
            Comment.save()
            return redirect(f'/writerblog/{_id}')
    else:
        form = CommentForm()
 
    context = {
            'data':data,
            'form':form,
            'comments':comments
        }
    return render(request,'writerdetailview.html',context)

@login_required
def WriterBloggerDetailView(request,_id):
    try:
        data =BlogModel.objects.get(id =_id)
        comments = CommentModel.objects.filter(blog = data).order_by('-date_added')
    except BlogModel.DoesNotExist:
        raise Http404('Data does not exist')
     
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment=form.save(commit=False)
            Comment.blog=data
            Comment.owned=request.user
            Comment.save()
            return redirect(f'/writerblogger/{_id}')
    else:
        form = CommentForm()
 
    context = {
            'data':data,
            'form':form,
            'comments':comments
        }
    return render(request,'writerdetailviewer.html',context)

@login_required
def writermanagecomment(request, _id):
    data =BlogModel.objects.get(id =_id)
    comments = CommentModel.objects.filter( owned=request.user, blog = data).order_by('-date_added')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment=form.save(commit=False)
            Comment.blog=data
            Comment.owned=request.user
            Comment.save()
            return HttpResponseRedirect(reverse('writermanagecomment', args=[data.id]))
    else:
        form = CommentForm()
    context = {'comments': comments, 'form':form, 'data':data}
    return render(request, 'writermanagecomment.html', context)

@login_required
def writereditcomment(request, _id):
    comment = CommentModel.objects.get(id=_id)
    blog=comment.blog
    if request.method != 'POST':
        form = CommentForm(instance=comment)
    else:
        form = CommentForm(instance=comment, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('writermanagecomment', args=[blog.id]))
    context = {'comment': comment, 'form': form}
    return render(request, 'writereditcomment.html', context)

@login_required
def writerdeletecomment(request, _id):
    deleter=CommentModel.objects.get(id=_id)
    blog=deleter.blog
    deleter.delete()
    return HttpResponseRedirect(reverse('writermanagecomment', args=[blog.id]))

@login_required
def writeraboutus(request):
    return render(request, 'writeraboutus.html')

@login_required
def writercontactus(request):
    return render(request, 'writercontactus.html')

@login_required
def writermanagepost(request):
    post = BlogModel.objects.filter(owner=request.user).order_by('-date_added')
    context = {'post':post}
    return render(request, 'writermanagepost.html', context)

@login_required
def writereditpost(request, _id):
    post = BlogModel.objects.get(id=_id)
    blog=post.blog
    if request.method != 'POST':
        form = PostForm(instance=post)
    else:
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('writerblogger', args=[post.id]))
    context = {'post': post, 'form': form}
    return render(request, 'writereditpost.html', context)

@login_required
def writeraddpost(request):
    if request.method != 'POST':
        form = PostForm() 
    else:
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = request.user
            new_post.save()
            return HttpResponseRedirect(reverse('writerblogs'))
    context = {'form': form}
    return render(request, 'writeraddpost.html', context)

@login_required
def writerdeletepost(request, _id):
    deletepost=BlogModel.objects.get(id=_id)
    blog=deletepost.blog
    deletepost.delete()
    return HttpResponseRedirect(reverse('writermanagepost'))

# Reader Views

@login_required
def ReaderBlogListView(request):
    dataset = BlogModel.objects.all().order_by('-date_added')
    paginator = Paginator(dataset, 5)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        dataset = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        dataset = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        dataset = paginator.page(paginator.num_pages)
    try:
        if request.method == 'POST':
            form = SearchForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                blog = BlogModel.objects.get(blog_title=title)
                return redirect(f'/readerblog/{blog.id}')
    except BlogModel.DoesNotExist:
        raise Http404
    else:
        form = SearchForm()
        context = {
            'dataset':dataset,
            'form':form,
            'page': page,
        }
        return render(request,'readerlistview.html', context)

def readerregister(request):
    msg = None
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_reader=True
            user.save()
            msg = 'user created'
            return redirect('login_view')
        else:
            msg = 'form is not valid'
    else:
        form = RegisterForm()
    return render(request,'readerregister.html', {'form': form, 'msg': msg})

@login_required
def ReaderBlogDetailView(request,_id):
    try:
        data =BlogModel.objects.get(id =_id)
        comments = CommentModel.objects.filter(blog = data).order_by('-date_added')
    except BlogModel.DoesNotExist:
        raise Http404('Data does not exist')
     
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment=form.save(commit=False)
            Comment.blog=data
            Comment.owned=request.user
            Comment.save()
            return redirect(f'/readerblog/{_id}')
    else:
        form = CommentForm()
 
    context = {
            'data':data,
            'form':form,
            'comments':comments
        }
    return render(request,'readerdetailview.html',context)

@login_required
def readermanagecomment(request, _id):
    data =BlogModel.objects.get(id =_id)
    comments = CommentModel.objects.filter( owned=request.user, blog = data).order_by('-date_added')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment=form.save(commit=False)
            Comment.blog=data
            Comment.owned=request.user
            Comment.save()
            return HttpResponseRedirect(reverse('readermanagecomment', args=[data.id]))
    else:
        form = CommentForm()
    context = {'comments': comments, 'form':form, 'data':data}
    return render(request, 'readermanagecomment.html', context)

@login_required
def readereditcomment(request, _id):
    comment = CommentModel.objects.get(id=_id)
    blog=comment.blog
    if request.method != 'POST':
        form = CommentForm(instance=comment)
    else:
        form = CommentForm(instance=comment, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('readermanagecomment', args=[blog.id]))
    context = {'comment': comment, 'form': form}
    return render(request, 'readereditcomment.html', context)

@login_required
def readerdeletecomment(request, _id):
    deleter=CommentModel.objects.get(id=_id)
    blog=deleter.blog
    deleter.delete()
    return HttpResponseRedirect(reverse('readermanagecomment', args=[blog.id]))

@login_required
def readeraboutus(request):
    return render(request, 'readeraboutus.html')

@login_required
def readercontactus(request):
    return render(request, 'readercontactus.html')

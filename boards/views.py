from email import message
from gc import get_objects
from re import template
from urllib import response
from django.shortcuts import redirect, render,get_object_or_404
from django.urls import reverse_lazy
from .models import Board
from django.http import HttpResponse,Http404
from django.contrib.auth.models import User
from .models import Post,Topic
from .forms import NewTopicForm,PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import View,CreateView,UpdateView,ListView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
# Create your views here.

# def home(request):
#     boards=Board.objects.all()
#     return render(request,'home.html',{'BOARDS':boards})  

class Home(ListView):
    model=Board
    context_object_name='BOARDS'
    template_name='home.html'

def board_topics(request,board_id,topic_id):
    board=get_object_or_404(Board,id=board_id)
    quertset=board.topics.order_by('-created_dt').annotate(comments=Count('posts'))
    page=request.GET.get('page',1)
    paginator=Paginator(quertset,10)
    try:
        topics=paginator.page(page)
    except PageNotAnInteger:
        topics=paginator.page(1)    
    except EmptyPage:
        topics=paginator.page(paginator.num_pages)

    if topic_id!=0:
        topic=get_object_or_404(Topic,id=topic_id)
        topic.delete()
        return redirect('board_topics',board_id=board.pk,topic_id=0)
    return render(request,'topics.html',{'board':board,'topics':topics})


@login_required
def new_topic(request,board_id):
    board=get_object_or_404(Board,id=board_id)
    # user=User.objects.first()
    if request.method=='POST':
        form=NewTopicForm(request.POST)
        if form.is_valid():
            topic=Topic.objects.create(
                subject=form.cleaned_data.get('subject'),
                board=board,
                created_by=request.user
            )
            post=Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('board_topics',board_id=board.pk,topic_id=0)
    else:
        form =NewTopicForm()

    return render(request,'new_topic.html',{'board':board,'form':form})

def topic_posts(request,board_id,topic_id):
    topic=get_object_or_404(Topic,board__pk=board_id,id=topic_id)
    topic.views+=1
    topic.save()
    return render(request,'topic_posts.html',{'topic':topic,'board_id':board_id})
@login_required
#functionl based view(FBW)
def reply_topic(request,board_id,topic_id):
    topic=get_object_or_404(Topic,board__pk=board_id,id=topic_id)
    if request.method=='POST':
        form=PostForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.topic=topic
            post.created_by=request.user
            post.save()
            return redirect('topic_posts',board_id=board_id,topic_id=topic_id)
    else: 
        form=PostForm()       
        return render(request,'reply_topic.html',{'topic':topic,'form':form})    
#class based view(CBV)
#convert my view to class and inside this class i divide my code into function to make it more clear
class Reply_Topic_CBV(View):        
    def post(self,request,board_id,topic_id):
        topic=get_object_or_404(Topic,board__pk=board_id,id=topic_id)
        form=PostForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.topic=topic
            post.created_by=request.user
            post.save()
            return redirect('topic_posts',board_id=board_id,topic_id=topic_id)
    
    def get(self,request,board_id,topic_id):
        topic=get_object_or_404(Topic,board__pk=board_id,id=topic_id)
        form=PostForm()       
        return render(request,'reply_topic.html',{'topic':topic,'form':form})    
#generic class based view
#there is built in classes in django can make everything just give it few inputs and every thing is okay    
class Reply_Topic_GCBV(CreateView):
    model=Post
    form_class=PostForm
    success_url=reverse_lazy('topics_posts')
    template_name='reply_topic'

@method_decorator(login_required,name='dispatch')
class PostUpdateView(UpdateView):
    model=Post
    fields=['message']#da bdl el form_class 3l42n m3mlt4 form ll update fa bdelo el fields 3la tol
    success_url=reverse_lazy('topic_posts')
    template_name='edit_post.html'
    pk_url_kwarg='post_id'
    context_object_name='post' 
    
    def form_valid(self,form):
        post=form.save(commit=False)
        post.updated_by=self.request.user
        post_updated_dt=timezone.now()
        post.save()
        return redirect('topic_posts',board_id=post.topic.board.pk,topic_id=post.topic.pk)

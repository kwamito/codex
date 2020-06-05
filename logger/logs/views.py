from django.shortcuts import render, redirect
from .forms import UserRegisterForm, ProfileCreateForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic import  CreateView, DetailView, ListView
from django.contrib.auth.mixins import  LoginRequiredMixin, UserPassesTestMixin
from .models import Profile, Log, Files, Project, Comment
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from pygments import highlight
import os
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer
# Create your views here.

def welcome(request):
    return render(request,'logs/welcome.html')

@login_required
def projects_page(request):
    if request.user:
        users_logs = Project.objects.filter(user=request.user)
    return render(request,'logs/home.html',{'logs':users_logs})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('name')
            messages.success(request,f'Your account has been created')
            return redirect('profile-create')
    else:
        form = UserRegisterForm()
    return render(request,'logs/signup.html',{'form':form})

class ProfileCreateView(LoginRequiredMixin,CreateView):
    model = Profile
    template_name = 'logs/profile-create.html'
    fields = ['avatar','bio']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ProfileDetailView(DetailView, LoginRequiredMixin):
    model = Profile
    template_name = 'logs/profile-detail.html'

@login_required
def profile_create(request):
    if request.method == 'POST':
        form = ProfileCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,f'Your profile has been created')
            return redirect('home')
    else:
        form = ProfileCreateForm()
    return render(request,'logs/profile-create.html',{'form':form})
@login_required
def profile_update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account info has been updated')
            return redirect('home')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'logs/profile_update.html',{'u_form':u_form,'p_form':p_form})

class CreateFile(CreateView, LoginRequiredMixin):
    model = Files
    template_name = 'logs/filer.html'
    fields = ['file_n','project','description']
    


class CreateProject(CreateView, LoginRequiredMixin):
    model = Project
    template_name = 'logs/project_create.html'
    fields = ['project_name','description','language']
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ProjectDetail(DetailView, LoginRequiredMixin, UserPassesTestMixin):
    model = Project
    template_name = 'logs/project-detail.html'

def project_detail(request,pk):
    users_project = Project.objects.get(id=pk)
    project_files = Files.objects.filter(project=users_project)
    if os.environ.get('DEV_ENV'):
        dev = True
    else:
        dev = False
    return render(request,'logs/project-detail.html',{'object':users_project,'files':project_files,'dev':dev})


def file_detail(request,name):
    #files = Filer.objects.get(file_n=name)
    filed = open('./media/files/'+name, 'r')
    op_fi = filed.read()
    if os.environ.get('DEV_ENV'):
        dev = True
    else:
        dev = False

    #lexer = get_lexer_by_name("python", stripall=True)
    #formatter = HtmlFormatter(linenos=True, cssclass="source")
    #result = highlight(op_fi, lexer, formatter)
    return render(request,'logs/file_det.html',{'file':op_fi,'name':name,'dev':dev})



class LogCreate(CreateView, UserPassesTestMixin, LoginRequiredMixin):
    model = Log
    template_name = 'logs/log-create.html'
    fields = ['code','title','image','image2']
    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class LogList(ListView):
    model = Log
    template_name = 'logs/log-list.html'
    context_object_name = 'logs'
    ordering = ['-date_created']

class LogDetail(DetailView):
    model = Log
    template_name = 'logs/log-detail.html'
    

def pin_detail(request, pk):
    pin = Pin.objects.get(id=pk)
    we = Comment.objects.filter(post=pin).order_by('-date_created')
    if request.method == 'POST':
        comment = request.POST.get('comm')
        c = Comment()
        c.user = request.user
        c.post = pin
        c.content = comment
        c.save()
    else:
        comment = None
    return render(request, 'pins/pin-detail.html',{'pin':pin,'co':comment,'we':we})

def log_detail(request, pk):
    log = Log.objects.get(id=pk)
    comms = Comment.objects.filter(log=log)
    if request.method == 'POST':
        comment = request.POST.get('comm')
        code = request.POST.get('code')
        rep = Comment()
        rep.user = request.user
        rep.log = log
        rep.reply = comment
        rep.code = code
        rep.save()
    else:
        comment = None
    return render(request,'logs/log-detail.html',{'log':log,'comment':comms})

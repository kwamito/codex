from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib import messages
from django.db.models import Q
from rest_framework import permissions
from pins.permissions import IsOwnerOrReadOnly
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from django.http import Http404
from rest_framework.parsers import JSONParser
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, CommentForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q
from .serializers import PostSerializer
from django.views.generic import RedirectView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Pin, Profile, Comment, FriendRequest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.response import Response

# Create your views here.
def home(request):
    is_liked = False
    if request.method == 'POST':
        post = get_object_or_404(Pin, id=request.POST.get('pin_id'))
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            is_liked = False
        else:
            post.likes.add(request.user)
            is_liked = True
    query = request.POST.get('search')
    if query:
        return redirect('search/{}'.format(query))
    else:
        pass

    if request.POST.get('clicked'):
        d = 'b'
    else:
        d = 'a'
    
    return render(request,'pins/home.html',{'pins':Pin.objects.all().order_by('-date_pinned'),'d':d,'is_liked':is_liked,'h':coms})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('name')
            messages.success(request,f'Your account has been created now create your profile')
            return redirect('profile-create')
    else:
        form = UserRegisterForm()
        username = 'nn'
    return render(request,'pins/register.html',{'form':form,'name':username})

def search(request, search):
    query = request.POST.get('search')
    if query:
        results = Pin.objects.filter(Q(title__icontains=query) | Q(pinner__username__icontains=query))
    else:
        results = Pin.objects.filter(title__icontains=search)
    return render(request,'pins/search.html',{'results':results})

class CreateProfile(CreateView, LoginRequiredMixin):
    template_name = 'pins/profile-create.html'
    model = Profile
    fields = ['user','avatar','preferences','info']


class ProfileDetailView(DetailView,LoginRequiredMixin):
    model = Profile
    template_name = 'pins/profile-detail.html'

class CreatePinView(CreateView, LoginRequiredMixin):
    model = Pin
    template_name = 'pins/pin-create.html'
    fields = ['title','category','image']
    
    def form_valid(self, form):
        form.instance.pinner = self.request.user
        return super().form_valid(form)

class PinDetailView(DetailView):
    model = Pin
    template_name = 'pins/pin-detail.html'

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


class UserPinListView(ListView):
    model = Pin
    template_name = 'pins/user_pins.html'
    context_object_name = 'pins'
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Pin.objects.filter(pinner=user).order_by('-date_pinned')

class UpdateProfileView(UpdateView,LoginRequiredMixin, UserPassesTestMixin):
    model = Profile
    template_name = 'pins/profile-create.html'
    fields = ['date_created','user','avatar','preferences','info']

def PinCre(request):
    title = request.POST.get('tite')
    drop = request.POST.get('drop')
    image = request.POST.get('image')
    if title:
        pin = Pin()
        pin.pinner = request.user
        pin.title = title
        pin.category = drop
        pin.image = image
        pin.save()
        return redirect('home')
    return render(request,'pins/signup.html')

def new(request):
    query = request.POST.get('search')
    if query:
        return redirect('search', query)
    else:
        pass
    return render(request, 'pins/whatsnew.html')


class PinUpdateView(UpdateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Pin
    template_name = 'pins/post-update.html'
    fields = ['category','likes','title','image']


def my_posts(request):
    my_post = Pin.objects.filter(pinner=request.user)
    return render(request,'pins/user_posts.html',{'my_post':my_post})


class CreateProfile(CreateView, LoginRequiredMixin):
    template_name = 'pins/profile-create.html'
    model = Profile
    fields = ['user','avatar','preferences','info']


class ProfileDetailView(DetailView,LoginRequiredMixin):
    model = Profile
    template_name = 'pins/profile-detail.html'


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    

    context = {
        'u_form':u_form,
        'p_form':p_form,
    }
    return render(request, 'pins/profile.html',context)



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




class UpdateProfileView(UpdateView):
    model = Profile
    template_name = 'pins/profile-create.html'
    fields = ['date_created','user','avatar','preferences','info']

def PinCre(request):
    title = request.POST.get('tite')
    drop = request.POST.get('drop')
    image = request.POST.get('image')
    if title:
        pin = Pin()
        pin.pinner = request.user
        pin.title = title
        pin.category = drop
        pin.image = image
        pin.save()
        return redirect('home')
    return render(request,'pins/signup.html')

def new(request):
    query = request.POST.get('search')
    if query:
        return redirect('search', query)
    else:
        pass
    return render(request, 'pins/whatsnew.html')


class PinUpdateView(UpdateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Pin
    template_name = 'pins/post-update.html'
    fields = ['category','likes','title','files']

@login_required
def my_posts(request):
    my_post = Pin.objects.filter(pinner=request.user)
    return render(request,'pins/user_posts.html',{'my_post':my_post})

class PostDeleteView(DeleteView):
    model = Pin
    template_name = 'pins/post-delete.html'
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == self.request.user:
            return True
        return False


def friend_req(request):
    reqs = FriendRequest.objects.filter(to_user=request.user)
    return render(request,'pins/friend_req.html',{'reqs':reqs})


class PostListApi(generics.ListCreateAPIView):
    queryset = Pin.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class PostDetailApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pin.objects.all()
    serializer_class = PostSerializer


class PinListApi(APIView):
    queryset = Pin.objects.all()
    def get(self, request, format=None):
        serializer = PostSerializer(queryset)
        return Response(serializer.data)

    def post(self,format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

